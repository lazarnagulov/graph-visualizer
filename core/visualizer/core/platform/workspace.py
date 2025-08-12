import sys

from jinja2 import Template
from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.api.service.plugin import Plugin
from visualizer.core.service.command_service import CommandService
from visualizer.core.service.plugin_service import PluginService
import visualizer.core.view.main_view as main_view
import os
from typing import Dict, List, Tuple, Optional

from visualizer.core.usecase import graph_util

from ..command.command_result import CommandResult, CommandStatus
from ..service.plugin_service import DATA_SOURCE_PLUGIN, VISUALIZER_PLUGIN

class Workspace:
    def __init__(self, plugin_service: PluginService):
        """
        Initialize the Workspace with plugin and command services.

        This constructor sets up the workspace by initializing internal references to the
        plugin and command services. It also initializes the visualizer and data source plugins
        to `None`, prepares an empty graph, and initializes an empty data file string.

        :param plugin_service: The service responsible for managing available plugins.
        :type plugin_service: PluginService
        """
        self.__plugin_service = plugin_service
        self.__visualizer_plugin: Optional[VisualizerPlugin] = None
        self.__data_source_plugin: Optional[DataSourcePlugin] = None
        self.__graph: Graph = Graph()
        self.__command_service = CommandService(self.generate_graph)
        self.__data_file_string: str = ""
        self.__graph_generated: bool = False  # Flag to prevent graph from being reloaded when empty

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
        old_identifier: str = self.__data_source_plugin.identifier()
        self.__data_source_plugin = self.__plugin_service.get_data_source_plugin(identifier)
        if old_identifier != identifier:
            self.generate_graph()

    def __set_default_plugins(self) -> None:
        """ Set plugins to first available. """
        if self.__visualizer_plugin is None and len(self.__plugin_service.plugins[VISUALIZER_PLUGIN]) > 0:
            self.__visualizer_plugin = self.__plugin_service.plugins[VISUALIZER_PLUGIN][0]
        if self.__data_source_plugin is None and len(self.__plugin_service.plugins[DATA_SOURCE_PLUGIN]) > 0:
            self.__data_source_plugin = self.__plugin_service.plugins[DATA_SOURCE_PLUGIN][0]

    @property
    def data_file_string(self) -> str:
        """
        Get the current data file string used by the data source plugin.

        :return: The string content of the data file.
        :rtype: str
        """
        return self.__data_file_string

    @data_file_string.setter
    def data_file_string(self, data_file_string: str) -> None:
        """
        Set the data file string to be used by the data source plugin.

        :param data_file_string: The string representation of the input data file.
        :type data_file_string: str
        """
        self.__data_file_string = data_file_string
        self.generate_graph()

    def execute_command(self, command_input: str) -> CommandResult:
        """
        Execute a command string on the current graph.

        This method delegates command execution to the command service, which handles
        parsing and running the command on the current graph instance. It returns a
        `CommandResult` indicating the outcome.

        :param command_input: The command string to execute.
        :type command_input: str

        :return: A `CommandResult` indicating the outcome of the execution.
        :rtype: CommandResult
        """
        return self.__command_service.execute_command(self.__graph, command_input)

    def generate_graph(self) -> None:
        """ Generate the graph using the currently selected data source plugin. """
        if self.__data_source_plugin and self.__data_file_string:
            self.__graph = self.__data_source_plugin.load(file_string=self.__data_file_string)
            self.__graph_generated = True

    def filter_graph(self, key: str, operator: str, value: any) -> str:
        try:
            graph_util.filter_graph(self.__graph, key, operator, value)
            return ""
        except Exception as e:
            return str(e)

    def search_graph(self, query: str) -> None:
        graph_util.search_graph(self.__graph, query)

    def render_main_view(self) -> Tuple[str, str, str]:
        """
        Render the main view. Generates a graph if empty.
        :return: (main_view_head, plugin_head, body) html string that should be included in page
        """
        if self.__visualizer_plugin is None or self.__data_source_plugin is None:
            self.__set_default_plugins()
        if not self.__graph_generated and (self.__graph is None or self.__graph.is_empty()):
            self.generate_graph()

        return main_view.render(self.__graph, self.__visualizer_plugin)


    def render_app_header(self) -> Tuple[str, str]:
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