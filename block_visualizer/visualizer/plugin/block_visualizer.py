import json
from typing import Tuple

from visualizer.api.model.graph import Graph
from visualizer.api.service.visualizer_plugin import VisualizerPlugin


class BlockVisualizer(VisualizerPlugin):

    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        print("Visualizing graph complexly")
        return "", f"<div>{json.dumps(graph)}</div>"

    def identifier(self) -> str:
        return "block_visualizer"

    def name(self) -> str:
        return "Block Visualizer"