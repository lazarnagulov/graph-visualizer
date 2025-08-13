from typing import List

from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.plugin_service import PluginService


class Platform:
    def __init__(self, plugin_service: PluginService):
        self.workspaces: List[Workspace] = [Workspace(plugin_service)]

    def get_selected_workspace(self) -> Workspace:
        return self.workspaces[0] # TODO: add workspace selection