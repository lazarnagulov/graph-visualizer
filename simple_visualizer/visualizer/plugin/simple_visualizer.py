import json
from typing import Tuple
import os
import sys

from visualizer.api.model.graph import Graph
from visualizer.api.service.visualizer_plugin import VisualizerPlugin


class SimpleVisualizer(VisualizerPlugin):

    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        print("Visualizing graph simply")
        with open(os.path.join(sys.prefix, 'templates/simple_visualizer_head_template.html'), 'r', encoding='utf-8') as file:
            head = file.read()
        return head, f"<div>{str(graph)}</div>"

    def identifier(self) -> str:
        return "simple_visualizer"

    def name(self) -> str:
        return "Simple Visualizer"