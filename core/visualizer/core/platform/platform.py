from typing import List

from visualizer.core.platform.workspace import Workspace
from visualizer.core.service.command_service import CommandService
from visualizer.core.service.plugin_service import PluginService


class Platform(object):
    def __init__(self, plugin_service: PluginService, command_service: CommandService):
        self.workspaces: List[Workspace] = [Workspace(plugin_service, command_service)]

    def get_selected_workspace(self) -> Workspace:
        return self.workspaces[0] # TODO: add workspace selection