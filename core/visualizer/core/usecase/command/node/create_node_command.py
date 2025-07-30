from typing import Any, Dict, Optional

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.usecase.command import Command
from visualizer.core.usecase.event_bus import EventBus

class CreateNodeCommand(Command):

    __slots__ = ["__graph", "__node_id", "__properties", "__event_bus", "__node"]

    def __init__(
        self,
        graph: Graph,
        node_id: str,
        properties: Dict[str, Any],
        event_bus: Optional[EventBus]
    ) -> None:
        self.__graph = graph
        self.__node_id = node_id
        self.__properties = properties
        self.__event_bus = event_bus
        self.__node = Node(self.__node_id, **self.__properties)

    def execute(self) -> None:
        self.__graph.insert_node(self.__node)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)

    def undo(self) -> None:
        self.__graph.remove_node(self.__node)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)
