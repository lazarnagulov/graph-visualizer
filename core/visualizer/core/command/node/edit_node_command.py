from typing import Any, Dict, Optional

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus
from visualizer.core.cli.exception.parser_exception import ParserError


class EditNodeCommand(Command):

    __slots__ = ["__graph", "__new_properties", "__old_properties", "__node"]

    def __init__(
        self,
        graph: Graph,
        node_id: str,
        new_properties: Dict[str, Any]
    ) -> None:
        self.__graph = graph
        self.__node: Optional[Node] = self.__graph.get_node(node_id)
        if self.__node is None:
            raise ValueError(f"node with id { node_id } not found")
        self.__old_properties = self.__node.properties.copy()
        self.__new_properties = new_properties

    def execute(self) -> None:
        self.__node.add_properties(self.__new_properties)

    def undo(self):
        self.__node.properties = self.__old_properties
