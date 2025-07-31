from typing import Optional, Dict, Any

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class EditEdgeCommand(Command):

    __slots__ = ["__graph", "__event_bus", "__edge", "__new_properties"]

    def __init__(
        self,
        graph: Graph,
        source: Node,
        destination: Node,
        properties: Dict[str, Any],
        event_bus: Optional[EventBus] = None
    ) -> None:
        self.__graph: Graph = graph
        self.__event_bus: EventBus = event_bus
        self.__edge: Edge = self.__graph.get_edge(source, destination)
        self.__new_properties: Dict[str, Any] = properties
        self.__old_properties: Dict[str, Any] = self.__edge.properties.copy()

    def execute(self) -> None:
        self.__edge.add_properties(**self.__new_properties)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)

    def undo(self) -> None:
        self.__edge.properties = self.__old_properties
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)
