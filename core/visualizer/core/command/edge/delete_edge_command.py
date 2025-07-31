from typing import Optional

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class DeleteEdgeCommand(Command):

    __slots__ = ["__graph", "__edge", "__source", "__destination", "__event_bus", "__old_properties"]

    def __init__(self, graph: Graph, source: Node, destination: Node, event_bus: Optional[EventBus] = None):
        self.__graph: Graph = graph
        self.__source = source
        self.__destination = destination
        self.__edge = self.__graph.get_edge(source, destination)
        self.__old_properties = self.__edge.properties.copy()
        self.__event_bus = event_bus

    def execute(self) -> None:
        self.__graph.remove_edge(self.__source, self.__destination)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)

    def undo(self) -> None:
        self.__graph.insert_edge(Edge(self.__source, self.__destination, **self.__old_properties))
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)