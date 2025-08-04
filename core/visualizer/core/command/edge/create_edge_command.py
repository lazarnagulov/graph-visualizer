from typing import Dict, Any, Optional


from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.api.model.edge import Edge
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class CreateEdgeCommand(Command):

    __slots__ = ["__graph", "__source", "__destination", "__properties"]

    def __init__(
        self,
        graph: Graph,
        source: Node,
        destination: Node,
        properties: Dict[str, Any]
    ) -> None:
        self.__graph: Graph = graph
        self.__source: Node = source
        self.__destination: Node = destination
        self.__properties: Dict[str, Any] = properties

    def execute(self) -> None:
        self.__graph.insert_edge(Edge(self.__source, self.__destination, **self.__properties))

    def undo(self) -> None:
        self.__graph.remove_edge(self.__source, self.__destination)
