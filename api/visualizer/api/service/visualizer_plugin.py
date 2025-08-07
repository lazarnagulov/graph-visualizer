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

        All top-level elements included in the head must have the "plugin-visualizer-head" class:
            ``<style class="plugin-visualizer-head">...</style>``

            ``<script class="plugin-visualizer-head">...</script>``

        All visualized nodes should have a "node" class, and all edges a "link" class.

        :param graph: The graph to visualize.
        :param kwargs: Arbitrary keyword arguments for customization (e.g., layout options).
        :type graph: Graph
        :type kwargs: any
        :return: A tuple containing the HTML head and body for the visualization.
        :rtype: Tuple[str, str]
        """
        ...