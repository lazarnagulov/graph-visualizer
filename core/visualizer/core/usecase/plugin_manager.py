from typing import Optional

from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.core.service.plugin_service import PluginService, VISUALIZER_PLUGIN, DATA_SOURCE_PLUGIN


class PluginManager:

    def __init__(self, plugin_service: PluginService) -> None:
        self.__plugin_service = plugin_service
        self.__visualizer_plugin: Optional[VisualizerPlugin] = None
        self.__data_source_plugin: Optional[DataSourcePlugin] = None

    @property
    def plugin_service(self) -> PluginService:
        return self.__plugin_service

    @property
    def visualizer_plugin(self) -> VisualizerPlugin:
        return self.__visualizer_plugin

    @property
    def data_source_plugin(self) -> DataSourcePlugin:
        return self.__data_source_plugin

    @visualizer_plugin.setter
    def visualizer_plugin(self, plugin: VisualizerPlugin) -> None:
        self.__visualizer_plugin = plugin

    @data_source_plugin.setter
    def data_source_plugin(self, plugin: DataSourcePlugin) -> None:
        self.__data_source_plugin = plugin

    def set_visualizer(self, identifier: str):
        self.__visualizer_plugin = self.__plugin_service.get_visualizer_plugin(identifier)

    def set_data_source(self, identifier: str):
        self.__data_source_plugin = self.__plugin_service.get_data_source_plugin(identifier)

    def set_defaults(self):
        if not self.__visualizer_plugin:
            self.__visualizer_plugin = self.__plugin_service.plugins[VISUALIZER_PLUGIN][0]
        if not self.__data_source_plugin:
            self.__data_source_plugin = self.__plugin_service.plugins[DATA_SOURCE_PLUGIN][0]