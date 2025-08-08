import ast
from _ast import FunctionDef, Call, ClassDef
from ast import NodeVisitor
from typing import Any, Optional, cast

from visualizer.api.model.edge import Edge
from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node


class CodeVisitor(NodeVisitor):

    __slots__ = ["__graph", "__current_function"]

    def __init__(self) -> None:
        self.__graph: Graph = Graph()
        self.__current_function: Optional[Node] = None

    @property
    def graph(self) -> Graph:
        return self.__graph

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        function_node: Node = Node(f"fn_{node.name}")
        function_node.add_property("name", node.name)
        function_node.add_property("args", [arg.arg for arg in node.args.args])
        # TODO: check for duplicates before inserting
        self.__graph.insert_node(function_node)

        if self.__current_function:
            edge: Edge = Edge(self.__current_function, function_node, defines=True)
            self.__graph.insert_edge(edge)

        previous_function = self.__current_function
        self.__current_function = function_node
        self.generic_visit(node)
        self.__current_function = previous_function

    def visit_Call(self, node: Call) -> Any:
        function_name: str = self.__get_function_name(node.func)
        call_node: Node = Node(f"fn_{function_name}")

        # TODO: check for duplicates before inserting
        self.__graph.insert_node(call_node)

        if self.__current_function:
            edge: Edge = Edge(self.__current_function, call_node, calls=True)
            self.graph.insert_edge(edge)

        self.generic_visit(node)

    def __get_function_name(self, func_node: ast.AST) -> str:
        if isinstance(func_node, ast.Name):
            return func_node.id
        else:
            return "<unknown>"