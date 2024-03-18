from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import FOAF, RDF


class FOAFFactory:
    _SUPPORTED_CLASSES = ['foaf:Agent', 'foaf:Group', 'foaf:Organization']

    def get_agent(self, rdf_graph: Graph):
        node_types = list(
            map(
                lambda x: x.n3(rdf_graph.namespace_manager),
                rdf_graph.objects(predicate=RDF.type, unique=True)
            )
        )

        if not set(node_types) <= set(self._SUPPORTED_CLASSES):
            raise NotImplementedError(
                "Required class types '%s' are not supported." %
                ', '.join(node_types))

        _supported_subclasses = set(self._SUPPORTED_CLASSES)
        _supported_subclasses.discard('foaf:Agent')

        # Having Organization and Group as type at the same time is an
        # error so we consider only the first in order of appearence
        if set(node_types) <= set(_supported_subclasses):
            if node_types[0] == 'foaf:Group':
                return FOAFGroup(rdf_graph=rdf_graph)
            elif node_types[0] == 'foaf:Organization':
                return FOAFOrganization(rdf_graph=rdf_graph)
        # There is only one type and is a generic 'foaf:Agent'
        elif set(node_types) == set(['foaf:Agent']):
            return FOAFAgent(rdf_graph)


class FOAFAgent(object):
    """A class representing a FOAF Agent."""

    _SUPPORTED_PROPERTIES = ['foaf:homepage', 'foaf:name']

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None):
        self._iri = iri
        self._dictionary = dictionary

        for _p in [_p.rpartition(':')[2] for _p in self._SUPPORTED_PROPERTIES]:
            setattr(FOAFAgent, f'_{_p}', None)

        # If an rdf Graph is provided, dictionary and iri parameters
        # are ignored
        if rdf_graph is not None:
            self._rdf = rdf_graph
            self._iri = next(self._rdf.subjects(predicate=RDF.type))

            for _p, _o in self._rdf.predicate_objects(self._iri):
                _p = _p.n3((self._rdf.namespace_manager))
                if _p in self._SUPPORTED_PROPERTIES:
                    _p = _p.partition(':')[2]
                    setattr(self, f'_{_p}', _o)

        else:
            self._rdf = Graph()
#         self._name = None

#         self._agent = None

            if self._iri is None:
                self._iri = BNode()
            else:
                self._iri = URIRef(self._iri)

#         if self._dictionary:
#             for p, o in self._dictionary.items():
#                 if p.lower() == 'type':
#                     self._rdf.add((self._iri, RDF.type, getattr(FOAF, o)))
#                 else:
#                     self._rdf.add((self._iri, getattr(FOAF, p), Literal(o)))
#
#         self._rdf.add((self._iri, RDF.type, FOAF.Agent))

    def rdf(self):
        return self._rdf

    def __repr__(self):
        return (f"<{self.__class__.__module__}.{self.__class__.__name__}"
                "{}".format(f", name: {self._name}>" if self._name is not None
                            else ">"))


class FOAFOrganization(FOAFAgent):
    """A class representing a FOAF Organization."""

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None):
        super().__init__(iri, dictionary, rdf_graph)
        self._rdf.set((self._iri, RDF.type, FOAF.Organization))


class FOAFGroup(FOAFAgent):
    """A class representing a FOAF Group."""

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None):
        raise NotImplementedError
        super().__init__(iri, dictionary, rdf_graph)
        self._rdf.set((self._iri, RDF.type, FOAF.Group))
