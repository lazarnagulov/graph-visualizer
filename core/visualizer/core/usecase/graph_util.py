import ast
import copy
from typing import List

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node

from core.visualizer.core.util.compare_util import CompareUtil, CompareException


def search_graph(graph: Graph, query: str) -> Graph:
    nodes = graph.get_nodes()
    query = query.lower()
    good_nodes = []
    for node in nodes:
        if query in node.id.lower() or __search_property(node.properties, query):
            good_nodes.add(node)
    return __recreate_graph(good_nodes, graph)

def __search_property(prop: any, query: str) -> bool:
    if isinstance(prop, dict):
        for key, value in prop.items():
            if query in key.lower():
                return True
            else:
                return __search_property(value, query)
        return False
    elif isinstance(prop, list) or isinstance(prop, tuple) or isinstance(prop, set):
        for value in prop:
            return __search_property(value, query)
        return False
    elif isinstance(prop, str):
        return query in prop.lower()
    else:
        return query in str(prop).lower()

def filter_graph(graph: Graph, key: str, operator: str, compare_value: str) -> Graph:
    nodes = graph.get_nodes()
    try:
        compare_value = ast.literal_eval(compare_value)
    except ValueError:
        pass # leave it as string

    try:
        CompareUtil.compare(operator, 1, 2)
    except CompareException as e:
        raise e

    good_nodes = []
    for node in nodes:
        if key.lower() == "id":
            property_value = node.id
        elif key in node.properties:
            property_value = node.properties[key]
        else:
            continue
        if CompareUtil.compare(operator, property_value, compare_value):
            good_nodes.append(node)

    return __recreate_graph(good_nodes, graph)

def __recreate_graph(nodes: List[Node], graph: Graph) -> Graph:
    new_graph = Graph()
    for node in nodes:
        new_graph.insert_node(copy.deepcopy(node)) # clone nodes to avoid referencing between graphs
    for node in nodes:
        incident_edges = graph.get_incident_edges(node)
        for edge in incident_edges:
            if new_graph.get_node(edge.destination.id) is None:
                continue
            new_edge = Edge(
                new_graph.get_node(edge.source.id),
                new_graph.get_node(edge.destination.id),
                **copy.deepcopy(edge.properties)
            )
            new_graph.insert_edge(new_edge)
    return new_graph
