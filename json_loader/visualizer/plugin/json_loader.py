import os
import json
from typing import Optional, Any, Dict, List, Tuple

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.api.service.data_source_plugin import DataSourcePlugin


class JsonLoader(DataSourcePlugin):

    __slots__ = ['__id_field', '__ref_prefix', '__nodes', '__unresolved_edges']

    CONFIG_PATH: str = os.path.join("..", "..", "config.json")
    DEFAULT_ID_FIELD: str = "@id"
    DEFAULT_REF_PREFIX: str = "&"

    def __init__(self) -> None:
        super().__init__()
        self.__id_field: str
        self.__ref_prefix: str
        self.__nodes: Dict[str, Node] = {}
        self.__unresolved_edges: List[Tuple[Node, str, str]] = []

        if not os.path.exists(self.CONFIG_PATH):
            self.__id_field = self.DEFAULT_ID_FIELD
            self.__ref_prefix = self.DEFAULT_REF_PREFIX
        else:
            with open(self.CONFIG_PATH) as f:
                config = json.load(f)
                self.__id_field = config['id-field']
                self.__ref_prefix = config['ref-prefix']

    @property
    def id(self) -> str:
        return self.__id_field

    @property
    def ref_prefix(self) -> str:
        return self.__ref_prefix

    def identifier(self) -> str:
        return "json_loader"

    def name(self) -> str:
        return "JsonLoader"

    def load(self, path: str, **kwargs) -> Graph:
        graph: Graph = Graph()

        if not path:
            raise ValueError("path must be provided")

        self.__generate_graph(graph, self.__load_json(path))
        self.__resolve_edges(graph)

        return graph

    def __insert_unresolved_edge(self, node: Node, ref_id: str, relation_name: str) -> None:
        self.__unresolved_edges.append((node, ref_id, relation_name))

    def __get_node_by_id(self, node_id: str) -> Optional[Node]:
        if not isinstance(node_id, str):
            raise TypeError("node id must be a string")
        return self.__nodes.get(node_id, None)

    def __insert_node(self, node_id: str, node: Node) -> None:
        if node_id in self.__nodes:
            raise ValueError(f"redefinition of { str(self.__nodes[node_id]) }")
        self.__nodes[node_id] = node

    @staticmethod
    def __load_json(path) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def __resolve_edges(self, graph: Graph) -> None:
        for node, ref_id, relation_name in self.__unresolved_edges:
            ref_node: Optional[Node] = self.__get_node_by_id(ref_id)
            if not ref_node:
                raise ValueError(f"invalid reference in JSON: {ref_id}")
            edge: Edge = Edge(node, ref_node)
            edge.add_property("relation", relation_name)
            graph.insert_edge(edge)

    def __generate_graph(
        self,
        graph: Graph,
        parsed_json: Any,
        parent_node: Optional[Node] = None,
        relation_name: Optional[str] = None
    ) -> None:
        if isinstance(parsed_json, dict):
            node: Node = Node()
            graph.insert_node(node)
            if parent_node:
                edge: Edge = Edge(parent_node, node, relation=relation_name)
                graph.insert_edge(edge)

            for key, value in parsed_json.items():
                if key == self.id:
                    node.id = value
                    self.__insert_node(value, node)
                    continue

                if isinstance(value, str) and value.startswith(self.ref_prefix):
                    ref_id: str = self.__get_reference_id(value)
                    ref_node: Optional[Node] = self.__get_node_by_id(ref_id)
                    if not ref_node:
                        self.__insert_unresolved_edge(node, ref_id, key)
                        continue

                    edge: Edge = Edge(node, ref_node, relation=key)
                    graph.insert_edge(edge)
                    continue

                if isinstance(value, dict) or isinstance(value, list):
                    self.__generate_graph(graph, value, node, key)
                elif isinstance(value, list):
                    for item in parsed_json:
                        self.__generate_graph(graph, item, node, key)
                else:
                    node.add_property(key, value)

        elif isinstance(parsed_json, list):
            for item in parsed_json:
                self.__generate_graph(graph, item, parent_node, relation_name)
        else:
            if isinstance(parsed_json, str) and parsed_json.startswith(self.ref_prefix):
                ref_id: str = self.__get_reference_id(parsed_json)
                ref_node: Optional[Node] = self.__get_node_by_id(ref_id)
                if not ref_node:
                    self.__insert_unresolved_edge(parent_node, ref_id, relation_name)
                    return

                edge: Edge = Edge(parent_node, ref_node, relation=relation_name)
                graph.insert_edge(edge)
                return

            if not self.__get_node_by_id(str(parsed_json)):
                node: Node = Node()
                node.id = parsed_json
                self.__insert_node(parsed_json, node)
                graph.insert_node(node)
                if parent_node and relation_name:
                    edge: Edge = Edge(parent_node, node, relation=relation_name)
                    graph.insert_edge(edge)

    def __get_reference_id(self, value: str) -> str:
        return value[len(self.ref_prefix):]

