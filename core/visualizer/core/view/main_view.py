from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.core.service.plugin_service import PluginService

from visualizer.api.model.graph import Graph

class MainView(object):
    def __init__(self, graph: Graph, visualizer: VisualizerPlugin):
        self.__graph = graph
        self.__visualizer = visualizer

    def render(self, **kwargs) -> (str, str):
        """
        Returns the required header and body html content that needs to be included in page
        in order to display the graph using the selected visualizer.
        :param visualizer_plugin_id: ID of the visualizer plugin that is used for displaying the graph.
        :param kwargs: Arguments for the visualizer plugin.
        :return: (header,body) html string that should be included in page.
        """

        # plugin: VisualizerPlugin = self.__plugin_service.get_visualizer_plugin(visualizer_plugin_id)
        _, html = self.__visualizer.visualize(graph=self.__graph, **kwargs)

        return "", html