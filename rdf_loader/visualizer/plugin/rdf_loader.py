from rdflib import Graph as RDFGraph, URIRef, Literal
from rdflib.namespace import RDF

from visualizer.api.model.graph import Graph
from visualizer.api.model.node import Node
from visualizer.api.model.edge import Edge
from visualizer.api.service.data_source_plugin import DataSourcePlugin


class RDFLoader(DataSourcePlugin):
    def __init__(self):
        self._graph = Graph()
        self._nodes_by_uri = {}

    def load(self, file_string: str, format: str = "turtle", **kwargs) -> Graph:
        self._graph.clear()
        self._nodes_by_uri.clear()

        rdf_graph = RDFGraph()
        rdf_graph.parse(data=file_string, format=format)

        for subj, pred, obj in rdf_graph:
            subj_node = self._get_or_create_node(subj)

            # Skip rdf:type as a separate node
            if pred == RDF.type and isinstance(obj, URIRef):
                subj_node.add_property("type", str(obj))
                continue

            pred_name = str(pred).split("#")[-1].split("/")[-1]

            if isinstance(obj, Literal):
                subj_node.add_property(pred_name, obj.value)
            elif isinstance(obj, URIRef):
                obj_node = self._get_or_create_node(obj)
                edge = Edge(subj_node, obj_node, predicate=pred_name)
                self._graph.insert_edge(edge)

        return self._graph

    def _get_or_create_node(self, uri: URIRef) -> Node:
        uri_str = str(uri)
        if uri_str not in self._nodes_by_uri:
            node = Node(uri_str)
            self._graph.insert_node(node)
            self._nodes_by_uri[uri_str] = node
        return self._nodes_by_uri[uri_str]

    def identifier(self) -> str:
        return "rdf_loader"

    def name(self) -> str:
        return "RDF Loader"


def main():
    path = "data/rdf/example1.ttl.txt"
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    loader = RDFLoader()
    g = loader.load(data)
    print(g)


if __name__ == "__main__":
    main()
