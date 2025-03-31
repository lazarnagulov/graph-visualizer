from typing import Dict, Tuple, Any

from .node import Node

class Edge:

    __slots__ = ['__source', '__destination', '__properties']

    def __init__(self, source: Node, destination: Node, **properties) -> None:
        self.__source: Node = source
        self.__destination: Node = destination
        self.__properties: Dict[str, Any] = properties

    @property
    def source(self) -> Node:
        return self.__source

    @source.setter
    def source(self, source: Node) -> None:
        if not isinstance(source, Node):
            raise TypeError(f'Error: expected Node but got { type(source) }')
        self.__source = source

    @property
    def destination(self) -> Node:
        return self.__destination

    @destination.setter
    def destination(self, destination: Node) -> None:
        if not isinstance(destination, Node):
            raise TypeError(f'Error: expected Node but got { type(destination) }')
        self.__destination = destination

    @property
    def properties(self) -> Dict[str, Any]:
        return self.__properties

    @properties.setter
    def properties(self, properties: Dict[str, Any]) -> None:
        if not isinstance(properties, dict):
            raise TypeError(f'Error: expected dict but got { type(properties) }')
        self.__properties = properties

    def add_property(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError(f'Error: expected str but got { type(key) }')
        self.__properties[key] = value

    def get_endpoints(self) -> Tuple[Node, Node]:
        return self.__source, self.__destination

    def __hash__(self) -> int:
        return hash((self.__source, self.__destination))

    def __str__(self) -> str:
        properties_str = ', '.join(f'{key}: {value}' for key, value in self.__properties.items())
        return f'Edge({self.__source}  --[{properties_str}]-> {self.__destination})'