import os
import sys
from typing import Tuple

from jinja2 import Template
from visualizer.api.model.graph import Graph
from visualizer.api.service.visualizer_plugin import VisualizerPlugin


def render(graph: Graph, visualizer: VisualizerPlugin, **kwargs) -> Tuple[str, str, str]:
    """
    Returns the required header and body html content that needs to be included in page
    in order to display the graph using the selected visualizer.
    :param graph: Graph to render.
    :param visualizer: Visualizer to use.
    :param kwargs: Arguments for the visualizer plugin.
    :return: (main_view_head, plugin_head, body) html string that should be included in page.
    """
    with open(os.path.join(sys.prefix, 'templates/main_view_head_template.html'), 'r', encoding='utf-8') as file:
        main_view_head = file.read()
    with open(os.path.join(sys.prefix, 'templates/main_view_body_template.html'), 'r', encoding='utf-8') as file:
        main_view_body = file.read()

    if not graph:
        graph = Graph()

    if visualizer:
        visualized_head, visualized_body = visualizer.visualize(graph=graph, **kwargs)
    else:
        visualized_head = ""
        visualized_body = "<p style=\"margin: 1rem\">No visualizer plugin</p>"

    if graph.is_empty() or visualized_body == "":
        visualized_body = "<p style=\"margin: 1rem\">No graph</p>"

    main_view_html = Template(main_view_body).render(visualized_body=visualized_body)
    return main_view_head, visualized_head, main_view_html
