from visualizer.api.model.graph import Graph
from visualizer.core.usecase.command import Command


class ClearCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def execute(self) -> None:
        raise NotImplemented("implement clear command execute")

    def undo(self) -> None:
        raise NotImplemented("implement clear command undo")