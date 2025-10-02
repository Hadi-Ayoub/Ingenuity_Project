#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Moteur
#  Created by Ingenuity i/o on 2025/10/02
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from Moteur import *

import random

# Settings
cols = 10
rows = 10
tile_size = 40
wall_thickness = 2

port = 5670
agent_name = "Moteur"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def generate_maze(x, y, grid, DIRECTIONS, OPPOSITE):
    stack = [(x, y)]
    grid[x][y]["visited"] = True

    while stack:
        cx, cy = stack[-1]
        current = grid[cx][cy]
        neighbors = []

        for dir, (dx, dy) in DIRECTIONS.items():
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and not grid[nx][ny]["visited"]:
                neighbors.append((dir, nx, ny))

        if neighbors:
            dir, nx, ny = random.choice(neighbors)
            current["walls"][dir] = False
            grid[nx][ny]["walls"][OPPOSITE[dir]] = False
            grid[nx][ny]["visited"] = True
            stack.append((nx, ny))
        else:
            stack.pop()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Moteur)
        
        if event == igs.AGENT_KNOWS_US and name == "Whiteboard":
             # Directions and their opposites
            DIRECTIONS = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0)
            }
            OPPOSITE = {
                "N": "S",
                "S": "N",
                "E": "W",
                "W": "E"
            }
            
            # Initialize the grid as a 2D list of cell dictionaries
            grid = [[{
                "visited": False,
                "walls": {"N": True, "S": True, "E": True, "W": True}
            } for _ in range(rows)] for _ in range(cols)]
            
            # Start maze from top-left
            generate_maze(0, 0, grid, DIRECTIONS, OPPOSITE)
            
            for x in range(cols):
                for y in range(rows):
                    cell = grid[x][y]
                    px = x * tile_size
                    py = y * tile_size

                    # Draw walls
                    if cell["walls"]["N"]:
                        igs.service_call("Whiteboard", "addShape", ("rectangle", px, py, px + tile_size, py, 'black', wall_thickness), "")
                    if cell["walls"]["S"]:
                        igs.service_call("Whiteboard", "addShape", ("rectangle", px, py + tile_size, px + tile_size, py + tile_size, 'black', wall_thickness), "")
                    if cell["walls"]["W"]:
                        igs.service_call("Whiteboard", "addShape", ("rectangle", px, py, px, py + tile_size, 'black', wall_thickness), "")
                    if cell["walls"]["E"]:
                        igs.service_call("Whiteboard", "addShape", ("rectangle", px + tile_size, py, px + tile_size, py + tile_size, 'black', wall_thickness), "")
                        
            # Entrance (top-left)
            igs.service_call("Whiteboard", "addShape", ("rectangle", 0, 0, tile_size, 0, 'white', wall_thickness), "")

            # Exit (bottom-right)
            exit_x = (cols - 1) * tile_size
            exit_y = rows * tile_size
            igs.service_call("Whiteboard", "addShape", ("rectangle", exit_x, exit_y - tile_size, exit_x + tile_size, exit_y - tile_size, 'white', wall_thickness), "")

        
        # add code here if needed
    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_class("Moteur")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = Moteur()

    igs.observe_agent_events(on_agent_event_callback, agent)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(0.1)

    igs.stop()
