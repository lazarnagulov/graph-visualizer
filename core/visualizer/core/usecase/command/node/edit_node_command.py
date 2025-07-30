from typing import Any, Dict, Optional

from visualizer.api.model.graph import Graph
from visualizer.core.usecase.command import Command
from visualizer.core.usecase.event_bus import EventBus


class EditNodeCommand(Command):

    __slots__ = ["__graph", "__node_id", "__new_properties", "__old_properties", "__event_bus"]

    def __init__(
        self,
        graph: Graph,
        node_id: str,
        new_properties: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.__graph = graph
        self.__node_id = node_id
        self.__new_properties = new_properties
        self.__old_properties = None
        self.__event_bus = event_bus

    def execute(self) -> None:
        raise NotImplemented("implement edit node command execute")

    def undo(self):
        raise NotImplemented("implement edit node command undo")