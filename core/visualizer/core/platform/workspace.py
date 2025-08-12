from visualizer.core.service.command_service import CommandService
from visualizer.core.service.plugin_service import PluginService
from typing import Tuple, Optional

from visualizer.core.usecase import graph_util

from ..command.command_result import CommandResult
from ..usecase.graph_manager import GraphManager
from ..usecase.plugin_manager import PluginManager
from ..view import app_header_view, main_view

class Workspace:

    def __init__(
        self,
        plugin_service: PluginService,
        command_service: Optional[CommandService] = None,
        graph_manager: Optional[GraphManager] = None
    ):
        """
        Initialize the Workspace with plugin and command services.

        This constructor sets up the workspace by initializing internal references to the
        plugin and command services. It also initializes the visualizer and data source plugins
        to `None`, prepares an empty graph, and initializes an empty data file string.

        :param plugin_service: The service responsible for managing available plugins.
        :type plugin_service: PluginService
        """
        self.__command_service = command_service or CommandService(self.generate_graph)
        self.__plugin_manager = PluginManager(plugin_service)
        self.__graph_manager = graph_manager or GraphManager(self.__plugin_manager)

    def set_visualizer_plugin(self, identifier: str) -> None:
        """
        Set visualizer plugin via its identifier.
        :param identifier: plugin identifier
        """
        self.__plugin_manager.set_visualizer(identifier)

    def set_data_source_plugin(self, identifier: str) -> None:
        """
        Set data source plugin via its identifier.
        :param identifier: plugin identifier
        """
        old_identifier: str = self.__plugin_manager.data_source_plugin.identifier()
        self.__plugin_manager.set_data_source(identifier)
        if old_identifier != identifier:
            self.generate_graph()

    def __set_default_plugins(self) -> None:
        """ Set plugins to first available. """
        self.__plugin_manager.set_defaults()

    @property
    def data_file_string(self) -> str:
        """
        Get the current data file string used by the data source plugin.

        :return: The string content of the data file.
        :rtype: str
        """
        return self.__graph_manager.data_file_string

    @data_file_string.setter
    def data_file_string(self, data_file_string: str) -> None:
        """
        Set the data file string to be used by the data source plugin.

        :param data_file_string: The string representation of the input data file.
        :type data_file_string: str
        """
        self.__graph_manager.data_file_string = data_file_string
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
        return self.__command_service.execute_command(self.__graph_manager.graph, command_input)

    def generate_graph(self) -> None:
        """ Generate the graph using the currently selected data source plugin. """
        self.__graph_manager.generate()

    def apply_filter(self, key: str, operator: str, value: any) -> str:
        try:
            graph_util.filter_graph(self.__graph_manager.graph, key, operator, value)
            return ""
        except Exception as e:
            return str(e)

    def search_graph(self, query: str) -> None:
        graph_util.search_graph(self.__graph_manager.graph, query)

    def render_main_view(self) -> Tuple[str, str, str]:
        """
        Render the main view. Generates a graph if empty.
        :return: (main_view_head, plugin_head, body) html string that should be included in page
        """
        if self.__plugin_manager.visualizer_plugin is None or self.__plugin_manager.data_source_plugin is None:
            self.__set_default_plugins()
        if not self.__graph_manager.graph_generated and (self.__graph_manager.graph is None or self.__graph_manager.graph.is_empty()):
            self.generate_graph()

        return main_view.render(self.__graph_manager.graph, self.__plugin_manager.visualizer_plugin)


    def render_app_header(self) -> Tuple[str, str]:
        """
        Returns the required header and body html content that needs to be included in page
        in order to display the app header.

        :return: (header,body) html string that should be included in page.
        """
        return app_header_view.render(self.__graph_manager.graph)