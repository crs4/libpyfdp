# pylint: disable=missing-module-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes

from rdflib import URIRef, BNode, IdentifiedNode
from rdflib.namespace import DCAT, DCTERMS, RDF  # , XSD, SKOS

import fdp.fairdatapoint
from fdp.dataset import Dataset
import fdp.version


class Catalog(Dataset):
    """Class representing a DCATv3 Catalog.

    :var uuid: the uuid that is assigned by the Fair Data Point
    :vartype uuid: str
    """

    URL_PATH = 'catalog'

    _PROPERTIES = ['creator', 'description', 'homepage', 'issued', 'license',
                   'publisher', 'title', 'version']

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 iri: str = None, uuid: str = None):
        super().__init__(fair_data_point, iri, uuid)

        # self._uuid = uuid
        # self._fair_data_point = fair_data_point or None

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
    # Catalog DCATv3 Class ispecific properties                               #
    ###########################################################################

    ###########################################################################
    @property
    def properties(self):
        """The DCATv3 Catalog class properties available.

        :returns: a list of the Catalog class properties available.
        :rtype: list of str
        """
        return self._PROPERTIES

    def inspect(self):
        """Retrieves the value of the class properties.

        :return: a dictionary with the class's properties.
        :rtype: dict
        """
        return {_p: getattr(self, _p) for _p in self._PROPERTIES}

    def __str__(self):
        return (f"<Catalog uuid={self._uuid}, title=\'{self._title}\', "
                f"version={self._version}, "
                "{}>".format("Tainted" if self._tainted else "NotTainted"))
