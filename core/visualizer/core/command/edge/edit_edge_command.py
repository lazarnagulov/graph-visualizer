from typing import Dict, Any

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.command import Command


class EditEdgeCommand(Command):

    __slots__ = ["__graph", "__edge", "__new_properties"]

    def __init__(
        self,
        graph: Graph,
        source: Node,
        destination: Node,
        properties: Dict[str, Any]
    ) -> None:
        self.__graph: Graph = graph
        self.__edge: Edge = self.__graph.get_edge(source, destination)
        if not self.__edge:
            raise ValueError(f"Cannot edit edge: No edge found with source '{source.id}' and destination '{destination.id}'.")
        self.__new_properties: Dict[str, Any] = properties
        self.__old_properties: Dict[str, Any] = self.__edge.properties.copy()

    def execute(self) -> None:
        self.__edge.add_properties(**self.__new_properties)

    def undo(self) -> None:
        self.__edge.properties = self.__old_properties
