from typing import Any, Dict, Optional, List, Tuple

from visualizer.api.model.graph import Graph
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.command import Command, CreateNodeCommand, DeleteNodeCommand, EditNodeCommand


def parse_command(graph: Graph, input_line: str) -> Command:
    tokens = input_line.strip().split()
    if not tokens:
        raise ParserError("no tokens provided")

    if tokens[0] == "create" and tokens[1] == "node":
        node_id, properties = __parse_id_and_properties(tokens[2:])
        return CreateNodeCommand(graph, node_id, properties, None)

    if tokens[0] == "delete" and tokens[1] == "node":
        return __parse_delete_node(graph, tokens[2:])

    if tokens[0] == "edit" and tokens[1] == "node":
        node_id, properties = __parse_id_and_properties(tokens[2:])
        return EditNodeCommand(graph, node_id, properties, None)

    raise ParserError("unknown command")

def __parse_delete_node(graph: Graph, tokens: List[str]) -> Command:
    if len(tokens) == 1 and tokens[0].startswith("--id="):
        node_id = tokens[0].split("--id=")[1]
        return DeleteNodeCommand(graph, node_id)
    raise ParserError("no node id provided")

def __parse_id_and_properties(tokens: List[str]) -> Tuple[str, Dict[str, Any]]:
    node_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        if tokens[i].startswith("--id="):
            node_id = tokens[i].split("--id=")[1]
        elif tokens[i].startswith("--property"):
            if i + 1 >= len(tokens):
                raise ParserError("expected key=value after --property")
            key_value = tokens[i + 1]
            if '=' not in key_value:
                raise ParserError(f"invalid property format: '{key_value}'")
            key, value = key_value.split("=", 1)
            properties[key] = value
            i += 1
        i += 1

    if node_id is None:
        raise ParserError("no node id provided")

    return node_id, properties