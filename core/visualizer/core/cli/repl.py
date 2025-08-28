import sys

from visualizer.api.model.graph import Graph
from visualizer.core.cli.command_parser import parse_command
from visualizer.core.service.command_service import CommandService


def __print_usage() -> None:
    print("""
            Graph CLI Usage:

              Node Commands:
                create node --id=<id> [--property <key=value>]...
                    - Creates a new node with optional properties
                edit node --id=<id> [--property <key=value>]...
                    - Edits an existing node's properties
                delete node --id=<id>
                    - Deletes a node by ID

              Edge Commands:
                create edge <source_id> <destination_id> [--property <key=value>]...
                    - Creates an edge between two nodes
                edit edge <source_id> <destination_id> [--property <key=value>]...
                    - Edits properties of an existing edge
                delete edge <source_id> <destination_id>
                    - Deletes the edge between two nodes

              Other:
                exit
                    - Exits the REPL
                help | --help | -h
                    - Shows this help message
        """)


def run_repl() -> None:
    argv = sys.argv
    if len(argv) == 2 and (argv[1] == "--help" or argv[1] == "-h"):
        __print_usage()
        return

    graph: Graph = Graph()
    command_service: CommandService = CommandService()

    while True:
        value = input(">> ")
        if value.lower().strip() == "exit":
            break
        elif value.lower().strip() == "help":
            __print_usage()
            continue
        try:
            cmd = parse_command(graph, value)
            command_service.execute(cmd)
            print(graph)
        except Exception as e:
            print("[COMMAND REPL] ", e)
