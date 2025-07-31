from typing import List, Optional, Dict, Any, Tuple

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.command import Command, CreateNodeCommand, DeleteNodeCommand, EditNodeCommand, CreateEdgeCommand, \
    EditEdgeCommand, DeleteEdgeCommand
from visualizer.core.service.command_service import CommandService


def parse_command(graph: Graph, input_line: str) -> Command:
    tokens = input_line.strip().split()
    if not tokens:
        raise ParserError("no tokens provided")

    match tokens[1]:
        case "node":
            return __parse_node_command(graph, tokens)
        case "edge":
            return __parse_edge_command(graph, tokens)
        case _:
            raise NotImplemented("implement general error parsing")

def __parse_edge_command(graph: Graph, tokens: List[str]) -> Command:
    source: Node = graph.get_node(tokens[2])
    destination: Node = graph.get_node(tokens[3])
    match tokens[0]:
        case "create":
            _, properties = __parse_properties(tokens[4:], False)
            return CreateEdgeCommand(graph, source, destination, properties, None)
        case "edit":
            _, properties = __parse_properties(tokens[4:], False)
            return EditEdgeCommand(graph, source, destination, properties, None)
        case "delete":
            return DeleteEdgeCommand(graph, source, destination, None)
        case _:
            raise ParserError(f"unknown command '{tokens[0]} node'")

def __parse_node_command(graph: Graph, tokens: List[str]) -> Command:
    match tokens[0]:
        case "create":
            node_id, properties = __parse_properties(tokens[2:])
            return CreateNodeCommand(graph, node_id, properties, None)
        case "edit":
            node_id, properties = __parse_properties(tokens[2:])
            return EditNodeCommand(graph, node_id, properties, None)
        case "delete":
            if tokens[2].startswith("--id="):
                node_id = tokens[2].split("--id=")[1]
                return DeleteNodeCommand(graph, node_id)
            raise ParserError("no node id provided")
        case _:
            raise ParserError(f"unknown command '{tokens[0]} node'")


def __parse_properties(tokens: List[str], require_id: bool = True) -> Tuple[Optional[str], Dict[str, Any]]:
    import ast
    node_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        if tokens[i].startswith("--id="):
            node_id = tokens[i].split("--id=", 1)[1]
        elif tokens[i] == "--property":
            if i + 1 >= len(tokens):
                raise ParserError("expected key=value after --property")
            key_value = tokens[i + 1]
            if '=' not in key_value:
                raise ParserError(f"invalid property format: '{key_value}'")
            key, value_str = key_value.split("=", 1)
            try:
                value = ast.literal_eval(value_str)
            except (ValueError, SyntaxError):
                value = value_str
            properties[key] = value
            i += 1
        i += 1

    if require_id and node_id is None:
        raise ParserError("no node id provided")

    return node_id, properties

def run_repl() -> None:
    graph: Graph = Graph()
    command_service: CommandService = CommandService()

    while True:
        value = input(">> ")
        if value.lower().strip() == "exit":
            break
        try:
            cmd = parse_command(graph, value)
            command_service.execute(cmd)
            print(graph)
        except Exception as e:
            print(e)
