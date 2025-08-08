from django.db import NotSupportedError
from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase import graph_util


class FilterCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph, key: str, operator: str, compare_value: str) -> None:
        self.__graph = graph
        self.__key = key
        self.__operator = operator
        self.__compare_value = compare_value

    def execute(self) -> None:
        graph_util.filter_graph(self.__graph, self.__key, self.__operator, self.__compare_value)

    def undo(self) -> None:
        raise NotSupportedError("Undo for FilterCommand is not supported. The previous graph state is not preserved.")
