from typing import List, Optional, Dict, Any, Tuple

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.command import (
    Command, CreateNodeCommand, DeleteNodeCommand, EditNodeCommand,
    CreateEdgeCommand, EditEdgeCommand, DeleteEdgeCommand, ClearCommand
)

def parse_command(graph: Graph, input_line: str) -> Command:
    tokens = input_line.strip().split()
    if not tokens:
        raise ParserError("No input provided. Please enter a command.")

    if len(tokens) == 1:
        if tokens[0] == "clear":
            return ClearCommand(graph)
        else:
            raise NotImplementedError("Incomplete command. A command requires more details (e.g., 'create node ...').")

    match tokens[1]:
        case "node":
            return __parse_node_command(graph, tokens)
        case "edge":
            return __parse_edge_command(graph, tokens)
        case _:
            raise ParserError(f"Unknown command target: '{tokens[1]}'. Expected 'node' or 'edge'.")


def __parse_edge_command(graph: Graph, tokens: List[str]) -> Command:
    if len(tokens) < 4:
        raise ParserError("Incomplete edge command. Expected syntax: '<action> edge <source> <destination> [--property key=value ...]'")

    source: Optional[Node] = graph.get_node(tokens[2])
    if not source:
        raise ValueError(f"Source node not found. Make sure both source and destination nodes exist.")

    destination: Optional[Node] = graph.get_node(tokens[3])
    if not destination:
        raise ValueError(f"Destination node not found. Make sure both source and destination nodes exist.")

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
            raise ParserError(f"Unknown edge command action: '{tokens[0]}'. Expected 'create', 'edit', or 'delete'.")


def __parse_node_command(graph: Graph, tokens: List[str]) -> Command:
    match tokens[0]:
        case "create":
            node_id, properties = __parse_properties(tokens[2:])
            if not node_id:
                raise ParserError("Missing node ID. Use '--id=<node_id>' to specify the ID.")
            return CreateNodeCommand(graph, node_id, properties)
        case "edit":
            node_id, properties = __parse_properties(tokens[2:])
            if not node_id:
                raise ParserError("Missing node ID. Use '--id=<node_id>' to specify the ID for editing.")
            return EditNodeCommand(graph, node_id, properties)
        case "delete":
            if len(tokens) > 2 and tokens[2].startswith("--id="):
                node_id = tokens[2].split("--id=", 1)[1]
                if not node_id:
                    raise ParserError("Empty node ID in '--id='. Provide a valid node ID.")
                return DeleteNodeCommand(graph, node_id)
            raise ParserError("Missing node ID. Use '--id=<node_id>' to specify which node to delete.")
        case _:
            raise ParserError(f"Unknown node command action: '{tokens[0]}'. Expected 'create', 'edit', or 'delete'.")


def __parse_properties(tokens: List[str]) -> Tuple[Optional[str], Dict[str, Any]]:
    import ast
    entity_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        if tokens[i].startswith("--id="):
            entity_id = tokens[i].split("--id=", 1)[1]
            if not entity_id:
                raise ParserError("Empty value provided for '--id='. Please specify a valid identifier.")
        elif tokens[i] == "--property":
            if i + 1 >= len(tokens):
                raise ParserError("Missing key=value pair after '--property'. Expected format: --property key=value")
            key_value = tokens[i + 1]
            if '=' not in key_value:
                raise ParserError(f"Invalid property format: '{key_value}'. Expected format: key=value")
            key, value_str = key_value.split("=", 1)
            try:
                value = ast.literal_eval(value_str)
            except (ValueError, SyntaxError):
                value = value_str
            properties[key] = value
            i += 1
        else:
            raise ParserError(f"Unrecognized token: '{tokens[i]}'. Did you mean to use '--id=' or '--property'?")
        i += 1

    return entity_id, properties
