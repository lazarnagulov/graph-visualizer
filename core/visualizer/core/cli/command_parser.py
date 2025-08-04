from typing import List, Optional, Dict, Any, Tuple

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.command import Command, CreateNodeCommand, DeleteNodeCommand, EditNodeCommand, CreateEdgeCommand, \
    EditEdgeCommand, DeleteEdgeCommand


def parse_command(graph: Graph, input_line: str) -> Command:
    tokens = input_line.strip().split()
    if not tokens:
        raise ParserError("no tokens provided")

    if len(tokens) == 1:
        raise NotImplementedError("implement general commands")

    match tokens[1]:
        case "node":
            return __parse_node_command(graph, tokens)
        case "edge":
            return __parse_edge_command(graph, tokens)
        case _:
            raise ParserError("unknown command")

def __parse_edge_command(graph: Graph, tokens: List[str]) -> Command:
    if len(tokens) < 4:
        raise ParserError("expected source and destination")

    source: Node = graph.get_node(tokens[2])
    destination: Node = graph.get_node(tokens[3])
    match tokens[0]:
        case "create":
            _, properties = __parse_properties(tokens[4:])
            return CreateEdgeCommand(graph, source, destination, properties)
        case "edit":
            _, properties = __parse_properties(tokens[4:])
            return EditEdgeCommand(graph, source, destination, properties)
        case "delete":
            return DeleteEdgeCommand(graph, source, destination)
        case _:
            raise ParserError(f"unknown command '{tokens[0]} node'")

def __parse_node_command(graph: Graph, tokens: List[str]) -> Command:
    match tokens[0]:
        case "create":
            node_id, properties = __parse_properties(tokens[2:])
            if not node_id:
                raise ParserError("no node id provided")
            return CreateNodeCommand(graph, node_id, properties)
        case "edit":
            node_id, properties = __parse_properties(tokens[2:])
            if not node_id:
                raise ParserError("no node id provided")
            return EditNodeCommand(graph, node_id, properties)
        case "delete":
            if len(tokens) > 2 and tokens[2].startswith("--id="):
                node_id = tokens[2].split("--id=")[1]
                return DeleteNodeCommand(graph, node_id)
            raise ParserError("no node id provided")
        case _:
            raise ParserError(f"unknown command '{tokens[0]} node'")


def __parse_properties(tokens: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    import ast
    entity_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        if tokens[i].startswith("--id="):
            entity_id = tokens[i].split("--id=", 1)[1]
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

    return entity_id, properties