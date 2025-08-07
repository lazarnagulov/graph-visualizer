from typing import Optional


from visualizer.api.model.graph import Graph
from visualizer.core.command import Command
from visualizer.core.usecase.event_bus import EventBus


class DeleteNodeCommand(Command):

    __slots__ = ["__graph"]

    def __init__(self, graph: Graph, node_id: str) -> None:
        self.__graph = graph
        self.__node = self.__graph.get_node(node_id)

    def execute(self) -> None:
        self.__graph.remove_node(self.__node)

    def undo(self) -> None:
        self.__graph.insert_node(self.__node)
