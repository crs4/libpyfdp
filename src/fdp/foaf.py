from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import FOAF, RDF


class FOAFFactory:
    _SUPPORTED_CLASSES = ['foaf:Agent', 'foaf:Group', 'foaf:Organization',
                          'foaf:Person']

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
            elif node_types[0] == 'foaf:Person':
                return FOAFPerson(rdf_graph=rdf_graph)
        # There is only one type and is a generic 'foaf:Agent'
        elif set(node_types) == set(['foaf:Agent']):
            return FOAFAgent(rdf_graph)


class FOAFAgent(object):
    """A class representing a FOAF Agent."""

    _SUPPORTED_PROPERTIES = ['foaf:homepage', 'foaf:name', 'foaf:member']

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None, name: str = None):
        self._dictionary = dictionary
        self._tainted = False

        self._rdf = rdf_graph or Graph()

        self._member_node = None

        for _p in [_p.rpartition(':')[2] for _p in self._SUPPORTED_PROPERTIES]:
            setattr(FOAFAgent, f'_{_p}', None)

        self._name = name or None

        # If an rdf Graph is provided, dictionary and iri parameters
        # are ignored
        if rdf_graph is not None:
            self._iri = next(self._rdf.subjects(predicate=RDF.type))

            for _p, _o in self._rdf.predicate_objects(self._iri):
                _p = _p.n3((self._rdf.namespace_manager))
                if _p in self._SUPPORTED_PROPERTIES:
                    _p = _p.partition(':')[2]
                    setattr(self, f'_{_p}', _o)

        elif self._dictionary:

            if 'iri' not in self._dictionary:
                self._iri = BNode()
            else:
                self._iri = URIRef(self._dictionary['iri'])

            for p, o in self._dictionary.items():
                if p.lower() == 'type':
                    self._rdf.add((self._iri, RDF.type, getattr(FOAF, o)))
                else:
                    self._rdf.add((self._iri, getattr(FOAF, p), Literal(o)))
        else:
            self._iri = BNode()

#         self._rdf.add((self._iri, RDF.type, FOAF.Agent))

    @property
    def iri(self):
        return self._iri

    @property
    def rdf(self):
        return self._rdf

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def homepage(self):
        """The ``foaf:homepage`` property."""
        return self._homepage

    @homepage.setter
    def homepage(self, homepage: str or Literal):
        if type(homepage) is str:
            self._homepage = homepage
        elif type(homepage) is Literal:
            self._homepage = str(homepage)
        else:
            raise TypeError

        self._rdf.add((
            self._iri,
            FOAF.homepage,
            URIRef(self._homepage)))

        self._tainted = True

    @property
    def name(self):
        """The ``foaf:name`` property."""
        return self._name

    @name.setter
    def name(self, name: str or Literal):
        if type(name) is str:
            self._name = name
        elif type(name) is Literal:
            self._name = str(name)
        else:
            raise TypeError

        self._rdf.add((
            self._iri,
            FOAF.name,
            Literal(self._name)))

        self._tainted = True

    def __str__(self):
        return (f"<{self.__class__.__module__}.{self.__class__.__name__}"
                f", iri: {self._iri}"
                "{}".format(f", name: {self._name}>" if self._name is not None
                            else ">"))

    def add_member(self, member):
        """Adds a member to a Group."""
        if self._member is None:
            self._member = {}
            self._member_node = BNode()

        self._member.update({member.iri: member})

        self._rdf.add((
            self._iri,
            FOAF.member,
            member.iri
        ))

        self._rdf += member.rdf

    @property
    def member(self) -> dict:
        """The members of the FOAF Organization."""
        return self._member


class FOAFPerson(FOAFAgent):
    """A class representing a FOAF Person."""

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None, name: str = None):
        super().__init__(iri, dictionary, rdf_graph, name)

        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Person))

    def add_member(self, member: FOAFAgent):
        raise NotImplementedError

    @property
    def members(self) -> dict:
        """Method not available for FOAF Person."""
        raise NotImplementedError


class FOAFOrganization(FOAFAgent):
    """A class representing a FOAF Organization."""

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None, name: str = None):
        super().__init__(iri, dictionary, rdf_graph, name)
        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Organization
        ))


class FOAFGroup(FOAFAgent):
    """A class representing a FOAF Group."""

    def __init__(self, iri: str = None, dictionary: dict = None,
                 rdf_graph: Graph = None, name: str = None):
        super().__init__(iri, dictionary, rdf_graph, name)
        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Group
        ))
