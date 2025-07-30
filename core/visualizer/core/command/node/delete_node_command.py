from typing import Optional


from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class DeleteNodeCommand(Command):

    __slots__ = ["__graph", "__node_id", "__event_bus"]

    def __init__(self, graph: Graph, node_id: str, event_bus: Optional[EventBus] = None) -> None:
        self.__graph = graph
        self.__node_id = node_id
        self.__event_bus = event_bus
        self.__node = self.__graph.get_node(node_id)

    def execute(self) -> None:
        self.__graph.remove_node(self.__node)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)

    def undo(self) -> None:
        self.__graph.insert_node(self.__node)
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)
