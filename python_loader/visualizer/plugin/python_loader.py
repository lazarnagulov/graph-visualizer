import ast
import os
from typing import Optional

from visualizer.api.exception.data_source_exception import MissingRequiredParameterError, InvalidParameterValueError
from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.plugin.code_visitor import CodeVisitor


class PythonLoader(DataSourcePlugin):

    def __init__(self):
        self.__visitor = CodeVisitor()

    def load(self, **kwargs) -> Graph:
        file_content: Optional[str] = kwargs.get('file_content', None)
        if not file_content:
            raise MissingRequiredParameterError("file_content must be provided")

        self.__visitor.graph = Graph()
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            raise InvalidParameterValueError(f"Provided file_content is not valid Python code.")
        self.__visitor.visit(tree)
        return self.__visitor.graph

    def identifier(self) -> str:
        return "python_loader"

    def name(self) -> str:
        return "Python Loader"


def main() -> None:
    path = os.path.join("..", "..", "..", "data", "python", "small_example.py")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    python_loader = PythonLoader()
    print(python_loader.load(code))


if __name__ == "__main__":
    main()
