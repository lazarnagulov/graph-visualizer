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
            with open(self.CONFIG_PATH, "r+", encoding="utf-8") as f:
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

    def load(self, file_string: Optional[str], **kwargs) -> Graph:
        if not file_string:
            raise ValueError("file_string must be provided")
        graph: Graph = Graph()
        self.__nodes = {}
        self.__unresolved_edges = []

        self.__generate_graph(graph, self.__load_json(file_string))
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
    def __load_json(file: str) -> Any:
        return json.loads(file)

    def __resolve_edges(self, graph: Graph) -> None:
        for node, ref_id, relation_name in self.__unresolved_edges:
            ref_node: Optional[Node] = self.__get_node_by_id(ref_id)
            if not ref_node:
                raise ValueError(f"invalid reference in JSON: {ref_id}")
            edge: Edge = Edge(node, ref_node, **{relation_name: True})
            graph.insert_edge(edge)

    def __generate_graph(
        self,
        graph: Graph,
        parsed_json: Any,
        parent_node: Optional[Node] = None,
        relation_name: Optional[str] = None
    ) -> None:
        match parsed_json:
            case dict():
                node: Node = Node()
                graph.insert_node(node)
                if parent_node:
                    edge: Edge = Edge(parent_node, node, **{relation_name: True})
                    graph.insert_edge(edge)

                for key, value in parsed_json.items():
                    self.__parse_dict_pair(graph, node, key, value)
            case list():
                for item in parsed_json:
                    self.__generate_graph(graph, item, parent_node, relation_name)
            case _:
                if self.__is_reference(parsed_json):
                    self.__parse_reference(graph, parent_node, relation_name, parsed_json)
                    return

                if not self.__get_node_by_id(str(parsed_json)):
                    node: Node = Node(parsed_json)
                    self.__insert_node(str(parsed_json), node)
                    graph.insert_node(node)
                    if parent_node and relation_name:
                        edge: Edge = Edge(parent_node, node, **{relation_name: True})
                        graph.insert_edge(edge)

    def __parse_dict_pair(self, graph: Graph, node: Node, key: str, value: Any) -> None:
        if key == self.id:
            node.id = value
            self.__insert_node(value, node)
            return

        if self.__is_reference(value):
            self.__parse_reference(graph, node, key, value)
            return

        if isinstance(value, dict) or isinstance(value, list):
            self.__generate_graph(graph, value, node, key)
        else:
            node.add_property(key, value)

    def __parse_reference(self, graph: Graph, parent_node: Node, key: str, value: str) -> None:
        ref_id: str = self.__get_reference_id(value)
        ref_node: Optional[Node] = self.__get_node_by_id(ref_id)
        if not ref_node:
            self.__insert_unresolved_edge(parent_node, ref_id, key)
            return

        edge: Edge = Edge(parent_node, ref_node, **{key: True})
        graph.insert_edge(edge)

    def __get_reference_id(self, value: str) -> str:
        return value[len(self.ref_prefix):]

    def __is_reference(self, value: Any) -> bool:
        return isinstance(value, str) and value.startswith(self.ref_prefix)


if __name__ == "__main__":
    loader: DataSourcePlugin = JsonLoader()
    path = os.path.join("..", "..", "..", "data", "json", "small_cyclic_data.json")
    with open(path, "r", encoding="utf-8") as f:
        file_str = f.read()
    print(loader.load(file=file_str))
