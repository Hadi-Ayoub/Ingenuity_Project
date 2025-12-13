#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  MessageBroadcast
#  Created by Ingenuity i/o on 2025/12/13
#
# no description


import sys
import time
import ingescape as igs
import socket
import threading
import signal


UDP_HOST = "127.0.0.1"
UDP_PORT = 6000
running = True 


def signal_handler(sig, frame):
    global running
    print("\n[ARRÊT] Signal reçu ! Nettoyage en cours...")
    running = False

# attacher le signal ctrl+c
signal.signal(signal.SIGINT, signal_handler)

# thread écoutant UDP
def udp_listening_thread():
    print(f"THREAD: Démarrage écoute UDP sur {UDP_HOST}:{UDP_PORT}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_HOST, UDP_PORT))
    sock.settimeout(0.5) 

    while running:
        try:
            data, addr = sock.recvfrom(1024)
            message_recu = data.decode('utf-8')
            
            # envoi vers ingescape
            igs.output_set_string("message_output", message_recu)
            print(".", end="", flush=True) 
            
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Erreur : {e}")
            break
            
    print("\nTHREAD: Fermeture du socket UDP.")
    sock.close()


def input_callback(io_type, name, value_type, value, my_data):
    pass

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_class("MessageBroadcast")
    igs.log_set_console(True)
    igs.output_create("message_output", igs.STRING_T, None)
    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    
    t = threading.Thread(target=udp_listening_thread, daemon=True)
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