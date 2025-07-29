import json
from typing import Tuple

from visualizer.api.model.graph import Graph
from visualizer.api.service.visualizer_plugin import VisualizerPlugin


class SimpleVisualizer(VisualizerPlugin):

    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        print("Visualizing graph simply")
        return "", f"<div>{json.dumps(graph)}</div>"

    def identifier(self) -> str:
        return "simple_visualizer"

    def name(self) -> str:
        return "Simple Visualizer"