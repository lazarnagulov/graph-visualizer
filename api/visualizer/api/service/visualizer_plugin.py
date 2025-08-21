from abc import abstractmethod
from typing import Tuple

from .plugin import Plugin
from ..model.graph import Graph


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
        All nodes that implement the "Drag & drop" functionality must be tagged with ``"drag"=true``.
        All nodes and edges that implement the zoom and pan functionalities must have a <g> element that is tagged
            with ``"zoom-and-pan"=true`` as an ancestor.
        All nodes and edges that implement the "Mouse over" functionality must be tagged with ``"mouse-over"=true``.

        Visualizer plugin must have exactly one <div> element tagged with ``"id"="[visualizer type]visualizer-main-div"``.
        Visualizer plugin must have exactly one <svg> element.
        It is recommended that these two elements be implemented so that the <svg> element is a child of the <div> element.
            Otherwise, correct behaviour of the program cannot be guaranteed.

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