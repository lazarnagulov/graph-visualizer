import os
import ast

from visualizer.api.model.graph import Graph
from visualizer.api.service.data_source_plugin import DataSourcePlugin
from visualizer.plugin.code_visitor import CodeVisitor


class PythonLoader(DataSourcePlugin):

    def __init__(self):
        super().__init__()
        self.__visitor = CodeVisitor()

    def load(self, code: str, **kwargs) -> Graph:
        tree = ast.parse(code)
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
