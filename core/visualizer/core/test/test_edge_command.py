from typing import Optional
from unittest import TestCase

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.core.cli.exception.parser_exception import ParserError
from visualizer.core.cli.command_parser import parse_command


class TestEdgeCommand(TestCase):

    def setUp(self):
        self.graph = Graph()
        self.node_1 = Node("1")
        self.node_2 = Node("2")
        self.node_3 = Node("3")
        self.node_4 = Node("4")
        self.graph.insert_nodes(self.node_1, self.node_2, self.node_3, self.node_4)
        self.graph.insert_edge(Edge(self.node_3, self.node_4, **{"existing": 123}))
        self.graph.insert_edge(Edge(self.node_4, self.node_4))


    def test_create_edge(self):
        command_input = "create edge 1 2 --property test1=test1"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_1, self.node_2)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.source, self.node_1)
        self.assertEqual(edge.destination, self.node_2)
        self.assertEqual(edge.properties, {"test1" : "test1"})

    def test_create_edge_without_properties(self):
        command_input = "create edge 2 3"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_2, self.node_3)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.source, self.node_2)
        self.assertEqual(edge.destination, self.node_3)
        self.assertEqual(edge.properties, {})

    def test_create_edge_without_source_and_destination_should_raise_parser_error(self):
        command_input = "create edge"

        with self.assertRaises(ParserError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Incomplete edge command. Expected syntax: '<action> edge <source> <destination> [--property key=value ...]'")

    def test_edit_edge_add_new_property(self):
        command_input = "edit edge 3 4 --property test1=123"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_3, self.node_4)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.source, self.node_3)
        self.assertEqual(edge.destination, self.node_4)
        self.assertTrue(edge.properties["test1"] == 123)

    def test_edit_edge_update_existing_property(self):
        command_input = "edit edge 3 4 --property existing=updated"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_3, self.node_4)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.source, self.node_3)
        self.assertEqual(edge.destination, self.node_4)
        self.assertTrue(edge.properties["existing"] == "updated")

    def test_edit_edge_that_does_not_exists_should_raise_value_error(self):
        command_input = "edit edge 6 9 --property existing=updated"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Source node not found. Make sure both source and destination nodes exist.")

    def test_delete_edge(self):
        command_input = "delete edge 4 4"

        parse_command(self.graph, command_input).execute()

        edge: Optional[Edge] = self.graph.get_edge(self.node_4, self.node_4)
        self.assertIsNone(edge)

    def test_delete_edge_that_does_not_exists_should_raise_value_error(self):
        command_input = "delete edge 96 24"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Source node not found. Make sure both source and destination nodes exist.")