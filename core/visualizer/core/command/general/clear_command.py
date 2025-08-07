from typing import Optional

from django.db import NotSupportedError
from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class ClearCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def execute(self) -> None:
        self.__graph.clear()

    def undo(self) -> None:
        raise NotSupportedError("Undo for ClearCommand is not supported. The previous graph state is not preserved.")
