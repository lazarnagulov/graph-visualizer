from collections import deque
from typing import Tuple, List, Set

from jinja2 import Template
from visualizer.api.model.node import Node
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.core.service.plugin_service import PluginService

from visualizer.api.model.graph import Graph
import os
import sys

def render(graph: Graph) -> Tuple[str, str]:
    """
    Returns the required head and body html content for the tree view.
    :param graph: Graph to render.
    :return: (head, body) html string that should be included in page.
    """
    with open(os.path.join(sys.prefix, 'templates/tree_view_head_template.html'), 'r', encoding='utf-8') as file:
        head = file.read()
    with open(os.path.join(sys.prefix, 'templates/tree_view_body_template.html'), 'r', encoding='utf-8') as file:
        body = file.read()

    if not graph or graph.is_empty():
        return head, '<div id="tree-view"><p style=\"margin: 1rem\">-----------</p></div>'

    graph_dict = graph.to_dict()

    # since tree view doesn't show edge data, we will remove it and embed it into nodes
    node_table: dict[str, int] = {node['id']: index for index, node in enumerate(graph_dict['nodes'])}
    for edge in graph_dict['edges']:
        source_node_index = node_table[edge['source']]
        source_node = graph_dict['nodes'][source_node_index]
        destination_node_index = node_table[edge['destination']]
        if 'children' not in source_node:
            source_node['children'] = []
        source_node['children'].append(destination_node_index)

    visited = set()
    graph_dict['start_nodes'] = []
    for node in graph.get_nodes():
        if node not in visited:
            graph_dict['start_nodes'].append(node_table[node.id])
            __bfs(graph, node, visited)

    graph_dict.pop('edges')

    rendered_body = Template(body).render(graph=graph_dict)
    return head, rendered_body

def __bfs(graph: Graph, start_node: Node, visited: Set[Node]) -> None:
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        visited.add(node)
        for edge in graph.get_incident_edges(node):
            if edge.destination not in visited:
                queue.append(edge.destination)
