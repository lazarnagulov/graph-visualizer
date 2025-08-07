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
        Head elements won't be updated unless the visualizer plugin is swapped.

        All visualized nodes should have the ``node`` class, and all edges the ``link`` class.
        To be identifiable, nodes should define an id attribute and edges source and destination attributes.
        All draggable nodes should be tagged with ``"drag"=true``.

        Visualizer plugin should define a global getGraphSimulation() function for accessing the d3 simulation object.

        For example::

            window.getGraphSimulation = () => simulation;

        :param graph: The graph to visualize.
        :param kwargs: Arbitrary keyword arguments for customization (e.g., layout options).
        :type graph: Graph
        :type kwargs: any
        :return: A tuple containing the HTML head and body for the visualization.
        :rtype: Tuple[str, str]
        """
        ...