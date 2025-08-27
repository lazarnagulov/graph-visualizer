from typing import Dict, Any

from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.core.usecase import graph_util
from visualizer.core.usecase.plugin_manager import PluginManager


class GraphManager:

    __slots__ = ["__plugin_manager", "__graph", "__graph_generated", "__data_file_string", "__properties"]

    def __init__(self, plugin_manager: PluginManager, **properties):
        self.__plugin_manager: PluginManager = plugin_manager
        self.__graph = Graph()
        self.__graph_generated = False
        self.__data_file_string = ""
        self.__properties: Dict[str, Any] = properties

    @property
    def data_source_plugin(self) -> DataSourcePlugin:
        return self.__plugin_manager.data_source_plugin

    @property
    def graph(self) -> Graph:
        return self.__graph

    @property
    def properties(self) -> Dict[str, Any]:
        return self.__properties

    @property
    def graph_generated(self) -> bool:
        return self.__graph_generated

    @property
    def data_file_string(self) -> str:
        return self.__data_file_string

    @data_file_string.setter
    def data_file_string(self, value: str) -> None:
        self.__data_file_string = value

    def set_data_file(self, file_string: str):
        self.__data_file_string = file_string
        self.generate()

    def generate(self, **kwargs):
        if len(kwargs) > 1:
            self.__properties = kwargs
        else:
            self.__properties = { 'file_content' : kwargs.get('file_content', '') }

        if self.data_source_plugin and self.__data_file_string:
            self.__graph = self.data_source_plugin.load(**self.__properties)
            self.__graph_generated = True

    def filter(self, key: str, operator: str, value: any) -> str:
        try:
            graph_util.filter_graph(self.__graph, key, operator, value)
            return ""
        except Exception as e:
            return str(e)

    def search(self, query: str):
        graph_util.search_graph(self.__graph, query)