import sys

from jinja2 import Template
from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.api.service.plugin import Plugin
from visualizer.core.service.plugin_service import PluginService
import visualizer.core.view.main_view as main_view
import os
from typing import Dict, List

from ..service.plugin_service import DATA_SOURCE_PLUGIN, VISUALIZER_PLUGIN

class Workspace(object):
    def __init__(self, plugin_service: PluginService):
        self.__plugin_service = plugin_service
        self.__visualizer_plugin: VisualizerPlugin | None = None
        self.__data_source_plugin: DataSourcePlugin | None = None
        self.__graph: Graph = Graph()

    def set_visualizer_plugin(self, identifier: str) -> None:
        """
        Set visualizer plugin via its identifier.
        :param identifier: plugin identifier
        """
        self.__visualizer_plugin = self.__plugin_service.get_visualizer_plugin(identifier)

    def set_data_source_plugin(self, identifier: str) -> None:
        """
        Set data source plugin via its identifier.
        :param identifier: plugin identifier
        """
        self.__data_source_plugin = self.__plugin_service.get_data_source_plugin(identifier)

    def __set_default_plugins(self) -> None:
        """ Set plugins to first available. """
        # TODO: add safety check in case there are no plugins
        if self.__visualizer_plugin is None:
            self.__visualizer_plugin = self.__plugin_service.plugins[VISUALIZER_PLUGIN][0]
        if self.__data_source_plugin is None:
            self.__data_source_plugin = self.__plugin_service.plugins[DATA_SOURCE_PLUGIN][0]

    def generate_graph(self) -> None:
        """ Generate the graph using the currently selected data source plugin. """
        # TODO: replace hardcoded path with file picker
        # TODO: add safety check in case data plugin was not set
        self.__graph = self.__data_source_plugin.load(path=os.path.join("..", "data", "json", "small_cyclic_data.json"))

    def render_main_view(self) -> (str,str):
        """
        Render the main view. Generates a graph if empty.
        :return: (header,body) html string that should be included in page
        """
        # TODO: add safety check in case visualizer plugin was not set
        if self.__visualizer_plugin is None or self.__data_source_plugin is None:
            self.__set_default_plugins()
        if self.__graph is None or self.__graph.is_empty():
            self.generate_graph()

        return main_view.render(self.__graph, self.__visualizer_plugin)


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
                                                   data_source_plugins=data_source_plugins_js,
                                                   selected_visualizer=self.__visualizer_plugin.identifier(),
                                                   selected_data_source=self.__data_source_plugin.identifier())
        return "", body_html