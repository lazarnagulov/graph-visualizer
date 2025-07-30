from visualizer.core.usecase.command import Command

from visualizer.api.model.graph import Graph


class EditEdgeCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def execute(self) -> None:
        raise NotImplemented("implement edit edge command execute")

    def undo(self) -> None:
        raise NotImplemented("implement edit edge command undo")
