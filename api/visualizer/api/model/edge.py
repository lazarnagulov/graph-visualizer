from typing import Dict, Tuple, Any

from .node import Node


class Edge:
    """
    Edge class that represents a directed edge between two nodes.

    This class stores the source and destination nodes of the edge, along with
    optional properties associated with the edge.
    """
    __slots__ = ['__source', '__destination', '__properties']

    def __init__(self, source: Node, destination: Node, **properties) -> None:
        """
        Initialize an Edge object with source and destination nodes and optional properties.

        :param source: The source node of the edge.
        :type source: Node
        :param destination: The destination node of the edge.
        :type destination: Node
        :param properties: Optional properties associated with the edge, passed as keyword arguments.

        :raises TypeError: If either source or destination is not a Node object.
        """
        if not isinstance(source, Node):
            raise TypeError(f"expected source to be a Node, but got { type(source) }")
        if not isinstance(destination, Node):
            raise TypeError(f"expected destination to be a Node, but got {type(destination)}")
        self.__source: Node = source
        self.__destination: Node = destination
        self.__properties: Dict[str, Any] = properties

    @property
    def source(self) -> Node:
        """
        Get the source node of the edge.

        :return: The source node.
        :rtype: Node
        """
        return self.__source

    @source.setter
    def source(self, source: Node) -> None:
        """
        Set the source node of the edge.

        :param source: The new source node for the edge.
        :type source: Node

        :raises TypeError: If the source is not a Node object.
        """
        if not isinstance(source, Node):
            raise TypeError(f'Error: expected Node, but got { type(source) }')
        self.__source = source

    @property
    def destination(self) -> Node:
        """
        Get the destination node of the edge.

        :return: The destination node.
        :rtype: Node
        """
        return self.__destination

    @destination.setter
    def destination(self, destination: Node) -> None:
        """
        Set the destination node of the edge.

        :param destination: The new destination node for the edge.
        :type destination: Node

        :raises TypeError: If the destination is not a Node object.
        """
        if not isinstance(destination, Node):
            raise TypeError(f'Error: expected Node but got { type(destination) }')
        self.__destination = destination

    @property
    def properties(self) -> Dict[str, Any]:
        """
        Get the properties associated with the edge.

        :return: The properties of the edge.
        :rtype: Dict[str, Any]
        """
        return self.__properties

    @properties.setter
    def properties(self, properties: Dict[str, Any]) -> None:
        """
        Set the properties of the edge.

        :param properties: A dictionary of properties to associate with the edge.
        :type properties: Dict[str, Any]

        :raises TypeError: If properties is not a dictionary.
        """
        if not isinstance(properties, dict):
            raise TypeError(f'Error: expected dict but got { type(properties) }')
        self.__properties = properties

    def add_property(self, key: str, value: Any) -> None:
        """
        Add a property to the edge.

        This method allows you to associate additional properties with the edge
        using a key-value pair. The key must be a string.

        :param key: The key for the property.
        :type key: str
        :param value: The value of the property.
        :type value: Any

        :raises TypeError: If the key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError(f'Error: expected str but got { type(key) }')
        self.__properties[key] = value

    def add_properties(self, **properties: Dict[str, Any]) -> None:
        """
        Add multiple properties to the edge.

        This method allows you to associate multiple key-value pairs with the edge
        at once. Each keyword argument is treated as a property, where the key must
        be a string and the value can be any type.

        :param properties: Arbitrary keyword arguments representing properties to add.
                           Each key must be a string.
        :type properties: Dict[str, Any]

        :raises TypeError: If any of the keys is not a string.
        """
        for key in properties:
            if not isinstance(key, str):
                raise TypeError(f'expected str but got {type(key)}')
        self.__properties.update(properties)

    def get_endpoints(self) -> Tuple[Node, Node]:
        """
        Get the source and destination nodes of the edge.

        This method returns a tuple containing the source node and the destination
        node of the edge.

        :return: A tuple containing the source and destination nodes.
        :rtype: Tuple[Node, Node]
        """
        return self.__source, self.__destination

    def __eq__(self, other: object) -> bool:
        """
        Compare this Edge object with another object for equality.

        This method checks if the other object is an `Edge` and determines their equality.
        Edges are considered equal if their source and destination are the same.

        :param other: The object to compare this Edge to.
        :type other: object

        :return: True if the edges are equal (i.e., have the same source and destination),
                 False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Edge):
            return False
        return self.source == other.source and self.destination == other.destination

    def __hash__(self) -> int:
        """
        Compute the hash value for the edge based on the source and destination nodes.

        This method ensures that two edges with the same source and destination
        nodes will have the same hash value, making the edge hashable and usable in
        hash-based collections like sets or dictionaries.

        :return: A hash value representing the edge.
        :rtype: int
        """
        return hash((self.__source, self.__destination))

    def __str__(self) -> str:
        """
        Create a string representation of the edge.

        This method returns a string that includes the source node, destination node,
        and the properties of the edge. It's useful for debugging and logging.

        :return: A string representing the edge and its properties.
        :rtype: str
        """
        properties_str = ', '.join(f'{key}: {value}' for key, value in self.__properties.items())
        return f'Edge({self.__source}  --[{properties_str}]-> {self.__destination})'