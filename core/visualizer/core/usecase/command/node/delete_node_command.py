from visualizer.core.usecase.command import Command

from visualizer.api.model.graph import Graph


class DeleteNodeCommand(Command):

    __slots__ = ["__graph, __node_id"]

    def __init__(self, graph: Graph, node_id: str) -> None:
        self.__graph = graph
        self.__node_id = node_id

    def execute(self) -> None:
        raise NotImplemented("implement delete node command execute")

    def undo(self) -> None:
        raise NotImplemented("implement delete node command undo")