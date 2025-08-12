from typing import Any, Dict

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.command import Command


class CreateNodeCommand(Command):

    __slots__ = ["__graph", "__node"]

    def __init__(
        self,
        graph: Graph,
        node_id: str,
        properties: Dict[str, Any]
    ) -> None:
        self.__graph = graph
        self.__node = Node(node_id, **properties)

    def execute(self) -> None:
        self.__graph.insert_node(self.__node)

    def undo(self) -> None:
        self.__graph.remove_node(self.__node)
