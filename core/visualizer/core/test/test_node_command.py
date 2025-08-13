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

        self.graph.insert_nodes(self.node, self.node_to_delete)

    def test_create_node(self):
        command_input = "create node --id=5 --property str=test1 --property boolean=True --property test3=123"

        parse_command(self.graph, command_input).execute()

        node = self.graph.get_node("5")
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "5")
        self.assertEqual(node.properties, {"str": "test1", "boolean": True, "test3": 123})

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

        self.assertEqual(str(exception.exception), "Missing node ID. Use '--id=<node_id>' to specify the ID.")


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

        self.assertEqual(str(exception.exception), "Missing node ID. Use '--id=<node_id>' to specify the ID for editing.")

    def test_edit_node_that_does_not_exist_should_raise_value_error(self):
        command_input = "edit node --id=500 --property test1=test1"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Cannot edit node: No node found with source ID '500'.")

    def test_delete_node(self):
        command_input = f"delete node --id={ self.node_to_delete_id }"

        parse_command(self.graph, command_input).execute()

        self.assertIsNone(self.graph.get_node(self.node_to_delete_id))

    def test_delete_node_without_id_should_raise_parser_error(self):
        command_input = "delete node"

        with self.assertRaises(ParserError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Missing node ID. Use '--id=<node_id>' to specify which node to delete.")

    def test_delete_node_that_does_not_exist_should_raise_value_error(self):
        command_input = f"delete node --id=500"

        with self.assertRaises(ValueError) as exception:
            parse_command(self.graph, command_input).execute()

        self.assertEqual(str(exception.exception), "Cannot remove node: Node with ID 'None' not found in the graph.")
