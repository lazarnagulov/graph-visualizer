import copy
import json
import pprint
from typing import Tuple
import os
import sys

from jinja2 import Template
from visualizer.api.model.graph import Graph, GraphDict
from visualizer.api.service.visualizer_plugin import VisualizerPlugin

from visualizer.api.model.edge import EdgeDict


class SimpleVisualizer(VisualizerPlugin):

    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        with open(os.path.join(sys.prefix, 'templates/simple_visualizer_head_template.html'), 'r', encoding='utf-8') as file:
            head = file.read()
        with open(os.path.join(sys.prefix, 'templates/simple_visualizer_body_template.html'), 'r', encoding='utf-8') as file:
            body_template = file.read()

        graph_dict: GraphDict = graph.to_dict()
        edge_table: dict[Tuple[str,str], int] = {(edge['source'], edge['destination']): index for index, edge in enumerate(graph_dict['edges'])}

        for key, index in edge_table.items():
            if index == -1:
                continue
            reverse_key = (key[1], key[0])
            if reverse_key in edge_table: # two edges between a pair of nodes
                graph_dict['edges'][index]['double'] = True
                index2 = edge_table[reverse_key]
                graph_dict['edges'][index2]['double'] = True
                edge_table[reverse_key] = -1 # mark as checked
            else:
                directed = True
            if key[0] == key[1]: # loop
                graph_dict['edges'][index]['loop'] = True

        for edge in graph_dict['edges']:    # d3 needs "target" key so it's easier to rename it here
            edge['target'] = edge['destination']
            edge.pop('destination')

        body = Template(body_template).render(graph=graph_dict, **kwargs)

        return head, body

    def identifier(self) -> str:
        return "simple_visualizer"

    def name(self) -> str:
        return "Simple Visualizer"