import ast
from _ast import FunctionDef, Call, ClassDef, expr
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

    @graph.setter
    def graph(self, graph: Graph) -> None:
        self.__graph = graph

    def visit_ClassDef(self, node: ClassDef) -> Any:
        class_node = Node(f"class_{node.name}")
        if not self.__graph.contains_node(class_node):
            class_node.add_properties({"name": node.name})
            self.__graph.insert_node(class_node)

        if self.__current_function:
            edge = Edge(self.__current_function, class_node, defines=True)
            self.__graph.insert_edge(edge)

        previous_function = self.__current_function
        self.__current_function = class_node
        self.generic_visit(node)
        self.__current_function = previous_function

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        function_node: Node = Node(f"fn_{node.name}")
        if not self.__graph.contains_node(function_node):
            function_node.add_properties({ "name": node.name,  "args" : [arg.arg for arg in node.args.args]})
            if node.returns:
                return_type = ast.unparse(node.returns)
                function_node.add_property("return_type", return_type)
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
        call_node: Optional[Node] = self.__graph.get_node(function_name)

        if not call_node:
            call_node = Node(function_name)
            self.__graph.insert_node(call_node)

        if self.__current_function:
            edge: Edge = Edge(self.__current_function, call_node, calls=True)
            self.graph.insert_edge(edge)

        self.generic_visit(node)

    def __get_function_name(self, func_node: expr) -> str:
        if isinstance(func_node, ast.Name):
            return f"fn_{func_node.id}"
        elif isinstance(func_node, ast.Attribute):
            attribute_parts = []
            while isinstance(func_node, ast.Attribute):
                attribute_parts.append(func_node.attr)
                func_node = func_node.value
            if isinstance(func_node, ast.Name):
                attribute_parts.append(func_node.id)
            full_name = '.'.join(reversed(attribute_parts))
            return f"fn_{full_name}"
        return "<unknown>"
