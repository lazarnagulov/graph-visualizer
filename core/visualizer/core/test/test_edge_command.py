from typing import Optional
from unittest import TestCase

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node

from core.visualizer.core.cli.command_parser import parse_command


class TestEdgeCommand(TestCase):

    def setUp(self):
        self.graph = Graph()
        self.node_1 = Node("1")
        self.node_2 = Node("2")

        self.graph.insert_nodes(self.node_1, self.node_2)

    def test_create_edge(self):
        command_input = "create edge 1 2 --property test1=test1"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_1, self.node_2)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.source, self.node_1)
        self.assertEqual(edge.destination, self.node_2)
        self.assertEqual(edge.properties, {"test1" : "test1"})



