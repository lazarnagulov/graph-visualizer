from typing import Dict, Any

from typing_extensions import Optional


class Node:
    """
    A Node class to represent a node in a graph with associated properties.

    This class allows for the creation of nodes with custom properties stored as
    a dictionary. The properties can be any key-value pairs where the key is a
    string, and the value can be of any type.
    """

    __slots__ = ['__properties']

    def __init__(self, **properties) -> None:
        """
        Initializes a Node object with properties.

        :param properties: A dictionary of properties where keys are strings
                           representing property names and values can be of any type.

        Example:
            node = Node(name="A", value=10)
            # Creates a node with properties {'name': 'A', 'value': 10}
        """
        self.__properties: Dict[str, Any] = properties

    @property
    def properties(self) -> Dict[str, Any]:
        """
        Get the properties of the Node.

        :return: A dictionary containing the properties of the node.
        :rtype: Dict[str, Any]
        """
        return self.__properties

    @properties.setter
    def properties(self, properties: Dict[str, Any]) -> None:
        """
        Set the properties of the Node.

        :param properties: A dictionary of properties to be set for the node.
        :type properties: Dict[str, Any]

        :raises TypeError: If the provided attributes are not a dictionary.
        """
        if not isinstance(properties, dict):
            raise TypeError(f"expected properties to be a dict, but got { type(properties) }")
        self.__properties = properties

    def add_property(self, key: str, value: Any) -> None:
        """
        Add a new property to the Node.

        :param key: The key (property name) of the property to be added.
        :type key: str
        :param value: The value of the property to be added.
        :type value: Any

        :raises TypeError: If the key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError(f"expected key to be a str, but got { type(key) }")

        self.__properties[key] = value

    def remove_property(self, key: str) -> Optional[Any]:
        """
        Remove a property from the Node by its key.

        :param key: The key (property name) of the property to be removed.
        :type key: str

        :return: The value of the removed property, or None if the key does not exist.
        :rtype: Optional[Any]

        :raises TypeError: If the key is not a string.
        """
        return self.__properties.pop(key, None)

    def __eq__(self, other: object) -> bool:
        """
        Compare this Node object with another object for equality.

        This method checks if the other object is a `Node` and compares their
        properties to determine equality. Nodes are considered equal if their
        properties (both keys and values) are the same.

        :param other: The object to compare this Node to.
        :type other: object

        :return: True if the nodes are equal (i.e., have the same properties),
                 False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Node):
            return False
        if self.properties.keys() == other.properties.keys():
            return False
        return all(self.properties[k] == other.properties[k] for k in self.properties)

    def __hash__(self) -> int:
        """
        Compute a hash value for the Node object.

        The hash value is based on the object's `id`, which ensures that the
        object’s hash is unique and consistent for the lifetime of the object.

        :return: A hash value representing the Node.
        :rtype: int
        """
        return hash(id(self))

    def __str__(self) -> str:
        """
        Create a string representation of the Node object.

        This method returns a string that includes all the properties of the
        Node in a readable format, useful for debugging or logging.

        :return: A string representing the Node and its properties.
        :rtype: str
        """
        properties_str = ', '.join(f'{key}: {value}' for key, value in self.__properties.items())
        return f'Node({ properties_str })'
