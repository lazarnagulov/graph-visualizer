from typing import Dict, Iterator, Optional

from .node import Node
from .edge import Edge

class Graph:

    def __init__(self) -> None:
        self.__outgoing: Dict[Node,Dict[Node, Edge]] = {}
        self.__incoming: Dict[Node,Dict[Node, Edge]] = {}

    @property
    def outgoing(self) -> Dict[Node,Dict[Node, Edge]]:
        return self.__outgoing

    @outgoing.setter
    def outgoing(self, value: Dict[Node, Dict[Node, Edge]]) -> None:
        if not isinstance(value, dict):
            raise TypeError(f"Error: expected dict got { type(value) }")
        self.__outgoing = value

    @property
    def incoming(self) -> Dict[Node,Dict[Node, Edge]]:
        return self.__incoming

    @incoming.setter
    def incoming(self, value: Dict[Node, Dict[Node, Edge]]) -> None:
        if not isinstance(value, dict):
            raise TypeError(f"Error: expected dict got { type(value) }")
        self.__incoming = value

    def get_node_count(self) -> int:
        return len(self.outgoing)

    def get_nodes(self) -> Iterator[Node]:
        yield from self.outgoing.keys()

    def insert_node(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise TypeError(f"Error: expected Node got { type(node) }")
        self.outgoing[node] = {}
        self.incoming[node] = {}

    def insert_nodes(self, *nodes: Node) -> None:
        for node in nodes:
            self.insert_node(node)

    def insert_edge(self, edge: Edge) -> None:
        if not isinstance(edge, Edge):
            raise TypeError(f"Error: expected Edge got { type(edge) }")
        self.outgoing[edge.source][edge.destination] = edge
        self.incoming[edge.destination][edge.source] = edge

    def insert_edges(self, *edges: Edge) -> None:
        for edge in edges:
            self.insert_edge(edge)

    def get_incident_edges(self, node: Node) -> Iterator[Edge]:
        for edge in self.outgoing[node].values():
            yield edge

    def get_edge(self, source: Node, destination: Node) -> Optional[Edge]:
        return self.outgoing[source].get(destination, None)

    def contains_edge(self, edge: Edge) -> bool:
        return self.get_edge(edge.source, edge.destination) is not None

    def contains_node(self, node: Node) -> bool:
        return node in self.outgoing

    def __str__(self) -> str:
        nodes_str = ''.join(f'{node}\n' for node in self.outgoing)
        edges_str = ''.join(
            f'{ edge }\n'
            for node_edges in self.outgoing.values()
            for edge in node_edges.values()
        )
        return f'Nodes:\n { nodes_str }\n  Edges:\n { edges_str }\n)'
