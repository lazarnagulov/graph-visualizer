import sys

from jinja2 import Template
from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.api.service.plugin import Plugin
from visualizer.core.service.plugin_service import PluginService
from visualizer.core.view.main_view import MainView
import os
from typing import Dict, List

from ..service.plugin_service import DATA_SOURCE_PLUGIN, VISUALIZER_PLUGIN

class Workspace(object):
    def __init__(self, plugin_service: PluginService):
        self.__plugin_service = plugin_service
        self.__visualizer_plugin: VisualizerPlugin | None = None
        self.__data_source_plugin: DataSourcePlugin | None = None
        self.__graph: Graph = Graph()

    @property
    def visualizer_plugin(self) -> VisualizerPlugin:
        return self.__visualizer_plugin

    @property
    def data_source_plugin(self) -> DataSourcePlugin:
        return self.__data_source_plugin

    @visualizer_plugin.setter
    def visualizer_plugin(self, visualizer_plugin: VisualizerPlugin):
        self.__visualizer_plugin = visualizer_plugin

    @data_source_plugin.setter
    def data_source_plugin(self, data_source_plugin: DataSourcePlugin):
        self.__data_source_plugin = data_source_plugin

    def generate_graph(self):
        # TODO: replace hardcoded path with file picker
        # TODO: add safety check in case data plugin was not set
        self.__graph = self.__data_source_plugin.load(path=os.path.join("..", "data", "json", "small_cyclic_data.json"))

    def generate_main_view(self):
        if self.__graph is None or self.__graph.is_empty():
            self.generate_graph()
        # TODO: add safety check in case visualizer plugin was not set
        return MainView(self.__graph, self.__visualizer_plugin)

    def render_app_header(self) -> (str, str):
        """
        Returns the required header and body html content that needs to be included in page
        in order to display the app header.

        :return: (header,body) html string that should be included in page.
        """

        with open(os.path.join(sys.prefix, 'templates/app_header_template.html'), 'r', encoding='utf-8') as file:
            body_template = file.read()

        visualizer_plugins: List[Plugin] = self.__plugin_service.plugins[VISUALIZER_PLUGIN]
        data_source_plugins: List[Plugin]  = self.__plugin_service.plugins[DATA_SOURCE_PLUGIN]

        visualizer_plugins_js: List[Dict[str,str]] = [
            {"name": plugin.name(), "id": plugin.identifier()}
            for plugin in visualizer_plugins]
        data_source_plugins_js: List[Dict[str,str]]  = [
            {"name": plugin.name(), "id": plugin.identifier()}
            for plugin in data_source_plugins]

        body_html = Template(body_template).render(visualizer_plugins=visualizer_plugins_js,
                                                   data_source_plugins=data_source_plugins_js)
        return "", body_html