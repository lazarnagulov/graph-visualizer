from typing import Any, Dict, Optional

from visualizer.api.model.graph import Graph
from visualizer.core.usecase.command import Command
from visualizer.core.usecase.command import CreateNodeCommand
from visualizer.core.usecase.command.exception.parser_exception import ParserError


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
        return CreateNodeCommand(graph, node_id, properties, None)


if __name__ == '__main__':
    g: Graph = Graph()
    cmd = parse_command(g, "create node --id=1234 --property Name=Lazar --property Surname=Nagulov")
    cmd.execute()
    print(g)