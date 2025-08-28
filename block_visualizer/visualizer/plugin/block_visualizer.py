import os
import sys

from typing import Tuple, List
from jinja2 import Template

from visualizer.api.model.graph import Graph, GraphDict
from visualizer.api.service.visualizer_plugin import VisualizerPlugin
from visualizer.api.model.edge import EdgeDict



class BlockVisualizer(VisualizerPlugin):
    def visualize(self, graph: Graph, **kwargs) -> Tuple[str, str]:
        with open(os.path.join(sys.prefix, 'templates/block_visualizer_head_template.html'), 'r', encoding='utf-8') as file:
            head = file.read()
        with open(os.path.join(sys.prefix, 'templates/block_visualizer_body_template.html'), 'r', encoding='utf-8') as file:
            body_template = file.read()
        
        if not graph or graph.is_empty():
            return head, ""
        
        graph_dict: GraphDict = graph.to_dict()
        self.__modify_data(graph_dict)

        body = Template(body_template).render(graph=graph_dict, **kwargs)

        return head, body

    def identifier(self) -> str:
        return "block_visualizer"

    def name(self) -> str:
        return "Block Visualizer"
    
    @staticmethod
    def __modify_data(graph_dict: GraphDict) -> None:
        edge_table: dict[Tuple[str,str], int] = {(edge['source'], edge['destination']): index for index, edge in enumerate(graph_dict['edges'])}

        directed = False
        for key, index in edge_table.items():
            if index == -1:
                continue

            reverse_key = (key[1], key[0])
            
            if key[0] == key[1]: # Is a loop.
                graph_dict['edges'][index]['loop'] = True
            elif reverse_key in edge_table: # Two edges are between a pair of nodes.
                index2 = edge_table[reverse_key]
                edge_table[reverse_key] = -1 # Mark it as checked.

                graph_dict['edges'][index]['double'] = True
                graph_dict['edges'][index2]['double'] = True
                
                if graph_dict['edges'][index]['properties'] != graph_dict['edges'][index2]['properties']:
                    directed = True
            else:
                directed = True

        graph_dict['directed'] = directed
        new_edges: List[EdgeDict] = []

        # If the graph is not directed, we can remove all duplicate edges.
        if not directed:
            for key, index in edge_table.items():
                if index == -1:
                    continue
                
                new_edges.append(graph_dict['edges'][index])
            
            graph_dict['edges'] = new_edges

        # D3 needs the "target" key, so it's easier to rename it here.
        for edge in graph_dict['edges']:
            edge['target'] = edge['destination']
            edge.pop('destination')