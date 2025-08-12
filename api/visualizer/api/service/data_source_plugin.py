from abc import abstractmethod

from .plugin import Plugin
from ..model.graph import Graph


class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading graph data from a specific data source.
    """

    @abstractmethod
    def load(self, **kwargs) -> Graph:
        """
        Loads data from the data source and returns it as a Graph.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: any
        :return: A Graph from the data source.
        :rtype: Graph
        """
        ...
