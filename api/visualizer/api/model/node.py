from typing import Dict, Any

from typing_extensions import Optional


class Node:

    __slots__ = ['__properties']

    def __init__(self, **properties) -> None:
        self.__properties: Dict[str, Any] = properties

    @property
    def properties(self) -> Dict[str, Any]:
        return self.__properties

    @properties.setter
    def properties(self, attributes: Dict[str, Any]) -> None:
        if not isinstance(attributes, dict):
            raise TypeError(f"Error: expected dict but got { type(attributes) }")
        self.__properties = attributes

    def add_property(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError(f"Error: expected str but got { type(key) }")
        self.__properties[key] = value

    def remove_property(self, key: str) -> Optional[Any]:
        if not isinstance(key, str):
            raise TypeError(f"Error: expected str but got { type(key) }")
        return self.__properties.pop(key, None)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        if self.properties.keys() == other.properties.keys():
            return False
        return all(self.properties[k] == other.properties[k] for k in self.properties)

    def __hash__(self) -> int:
        return hash(id(self))

    def __str__(self) -> str:
        properties_str = ', '.join(f'{key}: {value}' for key, value in self.__properties.items())
        return f'Node({ properties_str })'
