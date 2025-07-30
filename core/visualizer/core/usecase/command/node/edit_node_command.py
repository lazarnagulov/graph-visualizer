from typing import Any, Dict

from visualizer.core.usecase.command import Command

from visualizer.api.model.graph import Graph


class EditNodeCommand(Command):

    __slots__ = ["__graph", "__node_id", "__new_properties", "__old_properties"]

    def __init__(self, graph: Graph, node_id: str, new_properties: Dict[str, Any]) -> None:
        self.__graph = graph
        self.__node_id = node_id
        self.__new_properties = new_properties
        self.__old_properties = None

    def execute(self) -> None:
        raise NotImplemented("implement edit node command execute")

    def undo(self) -> None:
        raise NotImplemented("implement edit node command undo")