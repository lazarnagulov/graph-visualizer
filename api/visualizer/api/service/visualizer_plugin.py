from abc import abstractmethod
from typing import Tuple

from ..model.graph import Graph
from .plugin import Plugin


class VisualizerPlugin(Plugin):
    """
    An abstraction representing a plugin for visualising graph data.
    """
    @abstractmethod
    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        """
        Visualizes the given graph.

        :param graph: The graph to visualize.
        :param kwargs: Arbitrary keyword arguments for customization (e.g., layout options).
        :type graph: Graph
        :type kwargs: any
        :return: A tuple containing the HTML header and body for the visualization.
        :rtype: Tuple[str, str]
        """
        ...