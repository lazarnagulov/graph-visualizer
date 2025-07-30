from importlib.metadata import entry_points
from typing import List, Dict, cast

from visualizer.api.service.plugin import Plugin

from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin

DATA_SOURCE_PLUGIN: str = "visualizer.datasource"
VISUALIZER_PLUGIN: str = "visualizer.visualizer"

class PluginService:

    def __init__(self):
        self.plugins: Dict[str, List[Plugin]] = {}

    def load_plugins(self, group: str) -> None:
        """
        Dynamically loads plugins based on entrypoint group.
        """
        self.plugins[group] = []
        for ep in entry_points(group=group):
            p = ep.load()
            plugin: Plugin = p()
            self.plugins[group].append(plugin)

    def get_data_source_plugin(self, data_source_id: str) -> DataSourcePlugin:
        return cast(DataSourcePlugin, self.__get_plugin(DATA_SOURCE_PLUGIN, data_source_id))

    def get_visualizer_plugin(self, visualizer_id: str) -> VisualizerPlugin:
        return cast(VisualizerPlugin, self.__get_plugin(VISUALIZER_PLUGIN, visualizer_id))

    def __get_plugin(self, group: str, plugin_id: str) -> Plugin:
        return next(filter(lambda plugin: plugin.identifier() == plugin_id, self.plugins[group]))
