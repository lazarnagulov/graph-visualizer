from django.db import NotSupportedError
from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase import graph_util


class SearchCommand(Command):

    __slots__ = ["__graph", "__query"]

    def __init__(self, graph: Graph, query: str)-> None:
        self.__graph = graph
        self.__query = query

    def execute(self) -> None:
        graph_util.search_graph(self.__graph, self.__query)

    def undo(self) -> None:
        raise NotSupportedError("Undo for SearchCommand is not supported. The previous graph state is not preserved.")