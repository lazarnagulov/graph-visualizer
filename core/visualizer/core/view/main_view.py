from jinja2 import Template
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.core.service.plugin_service import PluginService

from visualizer.api.model.graph import Graph
import os
import sys

def render(graph: Graph, visualizer: VisualizerPlugin, **kwargs) -> (str, str):
    """
    Returns the required header and body html content that needs to be included in page
    in order to display the graph using the selected visualizer.
    :param graph: Graph to render.
    :param visualizer: Visualizer to use.
    :param kwargs: Arguments for the visualizer plugin.
    :return: (header,body) html string that should be included in page.
    """

    with open(os.path.join(sys.prefix, 'templates/main_view_template.html'), 'r', encoding='utf-8') as file:
        main_view_template = file.read()

    _, visualized_body = visualizer.visualize(graph=graph, **kwargs)
    main_view_html = Template(main_view_template).render(visualized_body=visualized_body)

    return "", main_view_html


# class MainView(object):
#     def __init__(self):
#         pass
#