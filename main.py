#!/usr/bin/env python3
# coding: utf-8

import sys
import time
import ingescape as igs
import socket
import threading
import signal

# Valeur par défaut, sera écrasée si un argument est fourni
TCP_HOST = "127.0.0.1"
TCP_PORT = 5000
running = True
explored_tiles = []
goal_reached = False
TILE_SIZE = 50


def draw_tile_on_whiteboard(x, y):
    screen_x = (x + 1) * TILE_SIZE + 10
    screen_y = (y + 1) * TILE_SIZE + 10
    print(f"Dessin Whiteboard -> x: {screen_x}, y: {screen_y}")

    igs.output_set_int("whiteboard_x", screen_x)
    igs.output_set_int("whiteboard_y", screen_y)
    igs.output_set_impulsion("whiteboard_impulse")


def signal_handler(sig, frame):
    global running
    print("\n[ARRÊT] Signal reçu ! Nettoyage en cours...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def tcp_listening_thread():
    global running

    print(f"THREAD: Démarrage écoute TCP sur {TCP_HOST}: ", TCP_PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((TCP_HOST, TCP_PORT))
        server.listen(1)
        server.settimeout(1.0)
    except Exception as e:
        print(f"Erreur bind socket: {e}")
        return

    try:
        while running:
            try:
                conn, addr = server.accept()
                print("Connexion Godot établie:", addr)
                conn.settimeout(0.5)

                while running:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            print("Godot déconnecté.")
                            break

                        messages = data.decode("utf-8").splitlines()
                        for line in messages:
                            if line == "GOAL_REACHED":
                                print("GOAL_REACHED")
                                igs.output_set_string("message_output", "GOAL_REACHED")
                            else:
                                try:
                                    parts = line.split(",")
                                    if len(parts) == 2:
                                        x, y = map(int, parts)
                                        print(f"Tuile reçue: x={x}, y={y}")
                                        explored_tiles.append((x, y))
                                        draw_tile_on_whiteboard(x, y)
                                except ValueError:
                                    print(f"Erreur de format reçu: {line}")

                    except socket.timeout:
                        continue  # Pas de données, on boucle pour vérifier running
                    except ConnectionResetError:
                        print("Connexion réinitialisée par Godot")
                        break

                conn.close()

            except socket.timeout:
                continue  # Timeout du accept(), on boucle pour vérifier running

    finally:
        print("\nTHREAD: Fermeture socket TCP.")
        server.close()


def input_callback(io_type, name, value_type, value, my_data):
    pass


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device ingescape_port [tcp_port]")
        exit(0)

    agent_name = sys.argv[1]
    network_device = sys.argv[2]
    igs_port = int(sys.argv[3])


    igs.agent_set_name(agent_name)
    igs.definition_set_class("MessageBroadcast")
    igs.log_set_console(True)
    igs.output_create("message_output", igs.STRING_T, None)
    igs.output_create("whiteboard_impulse", igs.IMPULSION_T, None)
    igs.output_create("whiteboard_x", igs.INTEGER_T, None)
    igs.output_create("whiteboard_y", igs.INTEGER_T, None)
    igs.output_create("whiteboard_size", igs.INTEGER_T, None)
    igs.output_set_int("whiteboard_size", TILE_SIZE)

    print(f"Démarrage Ingescape sur {network_device}:{igs_port}")
    #igs.start_with_device(network_device, igs_port)
    igs.start_with_ip(network_device, igs_port)

    t = threading.Thread(target=tcp_listening_thread, daemon=True)
    t.start()

    print("Agent démarré. Appuyez sur Ctrl+C pour quitter.")

    try:
        while running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    print("Arrêt d'Ingescape...")
    igs.stop()
    sys.exit(0)