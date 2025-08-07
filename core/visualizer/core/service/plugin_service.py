from importlib.metadata import entry_points
from typing import List, Dict, cast

from visualizer.api.service.plugin import Plugin

from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin

DATA_SOURCE_PLUGIN: str = "visualizer.datasource"
VISUALIZER_PLUGIN: str = "visualizer.visualizer"

class PluginService:

    def __init__(self):
        """
        Initialize the PluginService with an empty plugin registry.

        This constructor sets up a dictionary to store plugins grouped by their entry point names.
        """
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
        """
        Retrieve a data source plugin by its identifier.

        This method returns a `DataSourcePlugin` instance that matches the given ID
        from the loaded plugins in the `visualizer.datasource` group.

        :param data_source_id: The identifier of the desired data source plugin.
        :type data_source_id: str

        :return: The matching data source plugin.
        :rtype: DataSourcePlugin
        """
        return cast(DataSourcePlugin, self.__get_plugin(DATA_SOURCE_PLUGIN, data_source_id))

    def get_visualizer_plugin(self, visualizer_id: str) -> VisualizerPlugin:
        """
        Retrieve a visualizer plugin by its identifier.

        This method returns a `VisualizerPlugin` instance that matches the given ID
        from the loaded plugins in the `visualizer.visualizer` group.

        :param visualizer_id: The identifier of the desired visualizer plugin.
        :type visualizer_id: str

        :return: The matching visualizer plugin.
        :rtype: VisualizerPlugin
        """
        return cast(VisualizerPlugin, self.__get_plugin(VISUALIZER_PLUGIN, visualizer_id))

    def __get_plugin(self, group: str, plugin_id: str) -> Plugin:
        return next(filter(lambda plugin: plugin.identifier() == plugin_id, self.plugins[group]))
