# pylint: disable=missing-module-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes

from rdflib import Graph, URIRef, BNode, IdentifiedNode, Literal
from rdflib.namespace import DCAT, DCTERMS, RDF, FOAF  # , XSD, SKOS

import fdp.fairdatapoint
from fdp.dataset import Dataset
import fdp.version


class Catalog(Dataset):
    """Class representing a DCATv3 Catalog.

    :var uuid: the uuid that is assigned by the Fair Data Point
    :vartype uuid: str
    """

    URL_PATH = 'catalog'

    _WRITE_PROPERTIES = ['creator', 'description', 'homepage', 'issued',
                         'license', 'publisher', 'title', 'version']
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 iri: str = None, uuid: str = None):
        super().__init__(fair_data_point, iri, uuid)

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError((f'Type {type(iri)} not allowed for '
                                 '"iri" argument'))
        elif self._uuid is not None:
            self._iri = URIRef(
                f'{self._fair_data_point.url}/catalog/{self._uuid}')
        else:
            self._iri = BNode()

        self._tainted = False

        self._rdf.add((
            self._iri,
            RDF.type,
            DCAT.Catalog))

        if self._fair_data_point:
            self._rdf.add((
                self._iri,
                DCTERMS.isPartOf,
                URIRef(self._fair_data_point.url)))

    ###########################################################################
    # Catalog DCATv3 Class specific properties                                #
    ###########################################################################

    @property
    def homepage(self):
        """The ``foaf:homepage`` property."""
        return self._homepage

    @homepage.setter
    def homepage(self, homepage: str or Literal or Graph):
        if type(homepage) is Graph:
            homepage = homepage.value(self._iri, FOAF.homepage, any=False)

        if homepage is None:
            return
        elif type(homepage) is str:
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

    ###########################################################################
    def __str__(self):
        return (f"<Catalog uuid={self._uuid}, title=\'{self._title}\', "
                f"version={self._version}, "
                "{}>".format("Tainted" if self._tainted else "NotTainted"))
