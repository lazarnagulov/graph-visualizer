from typing import Optional

from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class ClearCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def execute(self) -> None:
        self.__graph = Graph()

    def undo(self) -> None:
        raise NotImplemented("implement clear command undo")