from typing import Dict, Iterator, Optional

from .node import Node
from .edge import Edge

class Graph:
    """
    Graph class to represent a graph with nodes and edges.

    The graph uses dictionaries to track outgoing and incoming edges for each node.
    - `outgoing` contains edges from a node to its destination nodes.
    - `incoming` contains edges to a node from its source nodes.
    """

    def __init__(self) -> None:
        """
        Initialize a Graph object with empty outgoing and incoming edge dictionaries.

        This method sets up two dictionaries:
        - `__outgoing`: A dictionary where each key is a `Node` object, and the value is
          another dictionary mapping destination `Node` objects to `Edge` objects.
        - `__incoming`: A dictionary where each key is a `Node` object, and the value is
          another dictionary mapping source `Node` objects to `Edge` objects.

        These dictionaries allow the graph to efficiently track the edges going out of
        or coming into a particular node.
        """
        self.__outgoing: Dict[Node,Dict[Node, Edge]] = {}
        self.__incoming: Dict[Node,Dict[Node, Edge]] = {}

    @property
    def outgoing(self) -> Dict[Node,Dict[Node, Edge]]:
        """
        Get the dictionary of outgoing edges for each node in the graph.

        This property returns a dictionary where the keys are `Node` objects (representing
        the source nodes) and the values are dictionaries mapping destination nodes to the
        corresponding `Edge` objects.

        :return: The dictionary of outgoing edges.
        :rtype: Dict[Node, Dict[Node, Edge]]
        """
        return self.__outgoing

    @outgoing.setter
    def outgoing(self, value: Dict[Node, Dict[Node, Edge]]) -> None:
        """
        Set the dictionary of outgoing edges for each node in the graph.

        This setter allows you to assign a custom dictionary of outgoing edges.
        The dictionary should map `Node` objects to other dictionaries, which map
        destination `Node` objects to corresponding `Edge` objects.

        :param value: A dictionary of outgoing edges, mapping each `Node` to a dictionary
                      of destination nodes and edges.
        :type value: Dict[Node, Dict[Node, Edge]]

        :raises TypeError: If the provided value is not a dictionary.
        """
        if not isinstance(value, dict):
            raise TypeError(f"expected value to ba a dict, but got { type(value) }")
        self.__outgoing = value

    @property
    def incoming(self) -> Dict[Node,Dict[Node, Edge]]:
        """
        Get the dictionary of incoming edges for each node in the graph.

        This property returns a dictionary where the keys are `Node` objects (representing
        the destination nodes) and the values are dictionaries mapping source nodes to the
        corresponding `Edge` objects.

        :return: The dictionary of incoming edges.
        :rtype: Dict[Node, Dict[Node, Edge]]
        """
        return self.__incoming

    @incoming.setter
    def incoming(self, value: Dict[Node, Dict[Node, Edge]]) -> None:
        """
        Set the dictionary of incoming edges for each node in the graph.

        This setter allows you to assign a custom dictionary of incoming edges.
        The dictionary should map `Node` objects to other dictionaries, which map
        source `Node` objects to corresponding `Edge` objects.

        :param value: A dictionary of incoming edges, mapping each `Node` to a dictionary
                      of source nodes and edges.
        :type value: Dict[Node, Dict[Node, Edge]]

        :raises TypeError: If the provided value is not a dictionary.
        """
        if not isinstance(value, dict):
            raise TypeError(f"expected value to be a dict, but got { type(value) }")
        self.__incoming = value

    def insert_node(self, node: Node) -> None:
        """
        Insert a node into the graph.

        This method adds a new node to the graph and initializes its outgoing and incoming
        edges as empty dictionaries. If the node is already in the graph, this will overwrite
        the existing edges for that node.

        :param node: The node to insert into the graph.
        :type node: Node

        :raises TypeError: If the provided node is not an instance of `Node`.
        """
        if not isinstance(node, Node):
            raise TypeError(f"expected Node, but got { type(node) }")
        self.outgoing[node] = {}
        self.incoming[node] = {}

    def insert_nodes(self, *nodes: Node) -> None:
        """
        Insert multiple nodes into the graph.

        This method inserts several nodes into the graph by calling `insert_node` for each
        node passed as arguments. Each node will have its outgoing and incoming edges
        initialized as empty dictionaries.

        :param nodes: The nodes to insert into the graph.
        :type nodes: Node

        :raises TypeError: If any of the provided arguments is not an instance of `Node`.
        """
        for node in nodes:
            self.insert_node(node)

    def insert_edge(self, edge: Edge) -> None:
        """
        Insert a directed edge into the graph.

        This method adds a directed edge from the source node to the destination node.
        If an edge already exists between these nodes, its properties are updated with the
        new edge's properties. Otherwise, the new edge is added to both the outgoing edges
        of the source node and the incoming edges of the destination node.

        :param edge: The directed edge to insert.
        :type edge: Edge

        :raises TypeError: If `edge` is not an instance of the `Edge` class.
        :raises ValueError: If either the source or destination node of the edge does not exist in the graph.
        """
        if not isinstance(edge, Edge):
            raise TypeError(f"expected Edge, but got { type(edge) }")

        if not self.contains_node(edge.source):
            raise ValueError(f"node {edge.source } not in graph.")

        if not self.contains_node(edge.destination):
            raise ValueError(f"node {edge.destination } not in graph.")

        existing_edge: Optional[Edge] = self.get_edge(edge.source, edge.destination)
        if existing_edge:
            existing_edge.add_properties(**edge.properties)
            return

        self.outgoing[edge.source][edge.destination] = edge
        self.incoming[edge.destination][edge.source] = edge

    def insert_edges(self, *edges: Edge) -> None:
        """
        Insert multiple edges into the graph.

        This method inserts several edges into the graph by calling `insert_edge` for each
        edge passed as arguments. It updates both the outgoing edges of the source node and
        the incoming edges of the destination node for each edge.

        :param edges: The edges to insert into the graph.
        :type edges: Edge

        :raises TypeError: If any of the provided arguments is not an instance of `Edge`.
        :raises ValueError: If any of the provided edge redefines existing edge.
        """
        for edge in edges:
            self.insert_edge(edge)

    def get_node_count(self) -> int:
        """
        Get the number of nodes in the graph.

        This method returns the total number of nodes in the graph by checking the length of
        the `outgoing` dictionary (since each key represents a node).

        :return: The number of nodes in the graph.
        :rtype: int
        """
        return len(self.outgoing)

    def get_nodes(self) -> Iterator[Node]:
        """
        Get an iterator over all nodes in the graph.

        This method returns an iterator over the keys of the `outgoing` dictionary, which
        represents all the nodes in the graph.

        :return: An iterator over the nodes in the graph.
        :rtype: Iterator[Node]
        """
        yield from self.outgoing.keys()

    def get_incident_edges(self, node: Node) -> Iterator[Edge]:
        """
        Get all edges incident to a node (outgoing edges from the node).

        This method returns an iterator over the edges where the given node is the source node.
        It iterates over the dictionary of outgoing edges for the node.

        :param node: The node for which to get the incident edges.
        :type node: Node

        :return: An iterator over the outgoing edges from the node.
        :rtype: Iterator[Edge]

        :raises KeyError: If the node is not in the graph.
        """
        if not self.contains_node(node):
            raise KeyError(f"node {node} is not in the graph.")

        for edge in self.outgoing[node].values():
            yield edge

    def get_edge(self, source: Node, destination: Node) -> Optional[Edge]:
        """
        Get the edge between two nodes if it exists.

        This method looks up an edge between the given source and destination nodes.
        If no such edge exists, it returns `None`.

        :param source: The source node of the edge.
        :type source: Node
        :param destination: The destination node of the edge.
        :type destination: Node

        :return: The edge from the source node to the destination node, or `None` if no such edge exists.
        :rtype: Optional[Edge]
        """
        return self.outgoing[source].get(destination, None)

    def contains_node(self, node: Node) -> bool:
        """
        Check if a node exists in the graph.

        This method checks if the given node is present in the graph by looking for it
        in the `outgoing` dictionary.

        :param node: The node to check for existence in the graph.
        :type node: Node

        :return: `True` if the node exists, `False` otherwise.
        :rtype: bool
        """
        return node in self.outgoing

    def contains_edge(self, edge: Edge) -> bool:
        """
        Check if an edge exists in the graph.

        This method checks if an edge from the source node to the destination node exists in
        the graph's outgoing edges.

        :param edge: The edge to check for existence in the graph.
        :type edge: Edge

        :return: `True` if the edge exists, `False` otherwise.
        :rtype: bool
        """
        return self.get_edge(edge.source, edge.destination) is not None

    def __str__(self) -> str:
        """
        Return a string representation of the graph, including all nodes and edges.

        The string representation is formatted as follows:
        - All nodes in the graph are listed, each on a new line.
        - All edges in the graph are listed, showing the source and destination node.

        Nodes and Edges are represented by their string representation (i.e., the `__str__` method
        of the `Node` and `Edge` class)

        :return: A formatted string representing the nodes and edges of the graph.
        :rtype: str
        """
        nodes_str = ''.join(f'{node}\n' for node in self.outgoing)
        edges_str = ''.join(
            f'{ edge }\n'
            for node_edges in self.outgoing.values()
            for edge in node_edges.values()
        )
        return f'Nodes:\n { nodes_str }\n  Edges:\n { edges_str }\n)'
