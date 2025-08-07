from visualizer.api.model.node import Node


class NodeHasEdgesError(Exception):
    """Exception raised when trying to remove a node that has edges attached."""
    def __init__(self, node: Node):
        super().__init__(f"Node {node} cannot be removed because it has edges attached.")
        self.node = node