from typing import Optional

from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class ClearCommand(Command):

    __slots__ = ["__graph", "__event_bus"]

    def __init__(self, graph: Graph, event_bus: Optional[EventBus] = None) -> None:
        self.__graph: Graph = graph
        self.__event_bus: EventBus = event_bus

    def execute(self) -> None:
        self.__graph = Graph()
        if self.__event_bus:
            self.__event_bus.emit("graph_updated", self.__graph)

    def undo(self) -> None:
        raise NotImplemented("implement clear command undo")