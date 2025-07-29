from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    An abstraction representing a plugin.
    """

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the data source plugin.

        :return: The unique identifier of the data source plugin.
        :rtype: str
        """
        ...

    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the data source plugin.

        :return: The name of the data source plugin.
        :rtype: str
        """
        ...
