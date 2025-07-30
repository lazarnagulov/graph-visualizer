from visualizer.api.model.graph import Graph
from visualizer.core.usecase.command import Command


class FilterCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph)-> None:
        self.__graph = graph

    def execute(self) -> None:
        raise NotImplemented("implement filter command execute")

    def undo(self) -> None:
        raise NotImplemented("implement filter command undo")