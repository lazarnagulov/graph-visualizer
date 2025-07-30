from typing import Any, Dict

from visualizer.core.usecase.command import Command

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node


class CreateNodeCommand(Command):

    __slots__ = ["__graph, __node_id, __properties"]

    def __init__(self, graph: Graph, node_id: str, properties: Dict[str, Any]) -> None:
        self.__graph = graph
        self.__node_id = node_id
        self.__properties = properties

    def execute(self) -> None:
        self.__graph.insert_node(Node(self.__node_id, **self.__properties))

    def undo(self) -> None:
        raise NotImplemented("implement create node undo")
