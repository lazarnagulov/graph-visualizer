from unittest import TestCase

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node

from visualizer.core.cli.command_parser import parse_command
from visualizer.core.cli.exception.parser_exception import ParserError


class TestNodeCommand(TestCase):

    def setUp(self):
        self.graph = Graph()

        self.node_id = "2"
        self.node_to_delete_id = "3"
        self.node_properties = {"property": 123}

        self.node = Node(self.node_id, **self.node_properties)
        self.node_to_delete = Node(self.node_to_delete_id, **self.node_properties)

        self.graph.insert_node(self.node)
        self.graph.insert_node(self.node_to_delete)

    def test_create_node(self):
        command_input = "create node --id=5 --property test1=test1 --property test2=test2 --property test3=test3"

        parse_command(self.graph, command_input).execute()

        node = self.graph.get_node("5")
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "5")
        self.assertEqual(node.properties, {"test1": "test1", "test2": "test2", "test3": "test3"})

    def test_create_node_without_properties(self):
        command_input = "create node --id=6"

        parse_command(self.graph, command_input).execute()

        node = self.graph.get_node("6")
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "6")
        self.assertEqual(node.properties, {})

    def test_create_node_without_id_should_raise_parser_error(self):
        command_input = "create node --property test1=test1"

        with self.assertRaises(ParserError) as exception:
            parse_command(self.graph, command_input).execute()

            self.assertEqual(str(exception.exception), "no node id provided")


    def test_edit_node_add_new_property(self):
        command_input = f"edit node --id={ self.node_id } --property test1=test1"

        parse_command(self.graph, command_input).execute()

        self.assertTrue(self.node.properties.get("test1"))

    def test_edit_node_update_existing_property(self):
        command_input = f"edit node --id={ self.node_id } --property property=new_one"

        parse_command(self.graph, command_input).execute()

        property_value = self.node.properties.get("property")
        self.assertIsNotNone(property_value)
        self.assertEqual(property_value, "new_one")

    def test_edit_node_without_id_should_raise_parser_error(self):
        command_input = "edit node --property test1=test1"

        with self.assertRaises(ParserError) as exception:
            parse_command(self.graph, command_input).execute()
            self.assertEqual(str(exception.exception), "no node id provided")

    def test_edit_node_that_does_not_exist_should_raise_value_error(self):
        command_input = "edit node --id=500 --property test1=test1"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

            self.assertEqual(str(exception.exception), "node with ID 500 not found")

    def test_delete_node(self):
        command_input = f"delete node --id={ self.node_to_delete_id }"

        parse_command(self.graph, command_input).execute()

        self.assertIsNone(self.graph.get_node(self.node_to_delete_id))

    def test_delete_node_without_id_should_raise_parser_error(self):
        command_input = "delete node"

        with self.assertRaises(ParserError) as exception:
            parse_command(self.graph, command_input).execute()

            self.assertEqual(str(exception.exception), "no node id provided")

    def test_delete_node_that_does_not_exist_should_raise_value_error(self):
        command_input = f"delete node --id=500"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

            self.assertEqual(str(exception.exception), "node with ID 500 not found")
