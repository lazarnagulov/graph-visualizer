from typing import Any, Dict, Optional

from visualizer.api.model.graph import Graph
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.command import Command, CreateNodeCommand, DeleteNodeCommand, EditNodeCommand
from visualizer.core.service.command_service import CommandService


def parse_command(graph: Graph, input_line: str) -> Command:
    tokens = input_line.strip().split()
    if not tokens:
        raise ParserError("no tokens provided")

    if tokens[0] == "create" and tokens[1] == "node":
        node_id: Optional[str] = None
        properties: Dict[str, Any] = {}
        i = 2
        while i < len(tokens):
            if tokens[i].startswith("--id="):
                node_id = tokens[i].split("--id=")[1]
            elif tokens[i].startswith("--property"):
                key, value = tokens[i + 1].split("=")
                properties[key] = value
                i += 1
            i += 1
        if node_id is None:
            raise ParserError("no node id provided")

        return CreateNodeCommand(graph, node_id, properties, None)

    if tokens[0] == "delete" and tokens[1] == "node":
        if len(tokens) == 3:
            if tokens[2].startswith("--id="):
                node_id = tokens[2].split("--id=")[1]
                return DeleteNodeCommand(graph, node_id)
        raise ParserError("no node id provided")

    if tokens[0] == "edit" and tokens[1] == "node":
        node_id: Optional[str] = None
        properties: Dict[str, Any] = {}
        i = 2
        while i < len(tokens):
            if tokens[i].startswith("--id="):
                node_id = tokens[i].split("--id=")[1]
            elif tokens[i].startswith("--property"):
                key, value = tokens[i + 1].split("=")
                properties[key] = value
                i += 1
            i += 1
        if node_id is None:
            raise ParserError("no node id provided")
        return EditNodeCommand(graph, node_id, properties, None)

if __name__ == '__main__':
    g: Graph = Graph()
    cmd_service = CommandService()

    cmd = parse_command(g, "create node --id=1234 --property Name=Lazar --property Surname=Nagulov")
    cmd_service.execute(cmd)
    cmd = parse_command(g, "edit node --id=1234 --property Name=NijeLazar --property Surname=Nagulov123 --property Age=22")
    cmd_service.execute(cmd)
    cmd_service.undo()
    print(g)
