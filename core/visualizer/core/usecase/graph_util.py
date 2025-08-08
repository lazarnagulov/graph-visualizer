import ast
import copy
from typing import List, Set

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node

from core.visualizer.core.util.compare_util import CompareUtil, CompareException


def search_graph(graph: Graph, query: str) -> None:
    nodes = graph.get_nodes()
    query = query.lower()
    good_nodes = set()
    for node in nodes:
        if query in node.id.lower() or __search_property(node.properties, query):
            good_nodes.add(node)
    __recreate_graph(good_nodes, graph)

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

def filter_graph(graph: Graph, key: str, operator: str, compare_value: str) -> None:
    nodes = graph.get_nodes()
    try:
        compare_value = ast.literal_eval(compare_value)
    except ValueError:
        pass # leave it as string

    try:
        CompareUtil.compare(operator, 1, 2)
    except CompareException as e:
        raise e

    good_nodes = set()
    for node in nodes:
        if key.lower() == "id":
            property_value = node.id
        elif key in node.properties:
            property_value = node.properties[key]
        else:
            continue
        if CompareUtil.compare(operator, property_value, compare_value):
            good_nodes.add(node)

    __recreate_graph(good_nodes, graph)

def __recreate_graph(nodes: Set[Node], graph: Graph) -> None:
    edges: List[Edge] = []
    for node in nodes:
        for edge in graph.get_incident_edges(node):
            if edge.destination in nodes:
                edges.append(edge)
    graph.clear()
    graph.insert_nodes(*nodes)
    graph.insert_edges(*edges)
