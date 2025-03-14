# pylint: disable=missing-module-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
import datetime
import json

from rdflib import URIRef, Literal, Graph, BNode, IdentifiedNode
from rdflib.namespace import DCTERMS, DCAT, Namespace, RDF

import fdp.fairdatapoint
from fdp.base import FairDataPointItem, SetEncoder

DQV = Namespace("http://www.w3.org/ns/dqv#")
SPDX = Namespace("http://spdx.org/rdf/terms#")


class Resource(FairDataPointItem):
    """Class representing a DCATv3 Cataloged Resource"""

    URL_PATH = "resource"
    CONTENT_TYPE = "text/turtle"

    _WRITE_PROPERTIES = [
        "creator",
        "description",
        "issued",
        "license",
        "publisher",
        "theme",
        "title",
        "version",
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
    ):
        super().__init__(fair_data_point)

        self._rdf = Graph()

        self._rdf.bind("dcat", DCAT)
        self._rdf.bind("dcterms", DCTERMS)
        self._rdf.bind("dqv", DQV)
        self._rdf.bind("spdx", SPDX)

        self._uuid = uuid

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError(
                    (f"Type {type(iri)} not allowed for " '"iri" argument')
                )
        elif self._uuid is not None:
            self._iri = URIRef(
                f"{self._fair_data_point.url}/resource/{self._uuid}"
            )
        else:
            self._iri = BNode()

        self._tainted = False

        self._rdf.add((self._iri, RDF.type, DCAT.Resource))

    @property
    def iri(self):
        """The iri of the Resource instance."""
        return self._iri

    @property
    def creator(self):
        """The ``dcterms:creator`` property."""
        return self._creator

    @creator.setter
    def creator(self, creator: str or dict or fdp.foaf.FOAFAgent):
        if isinstance(creator, str):
            self._creator = fdp.foaf.FOAFAgent()
            self._creator.name = creator

            self._rdf += self._creator.rdf

            self._tainted = True
        elif isinstance(creator, fdp.foaf.FOAFAgent):
            self._creator = creator
            self._rdf += self._creator.rdf
            self._tainted = True
        else:
            raise TypeError(
                ("creator must be a FOAFAgent's class instance " "or a string.")
            )

        self._rdf.add((self._iri, DCTERMS.creator, self._creator.iri))

    @property
    def description(self):
        """The ``dcterms:description`` property."""
        return self._description

    @description.setter
    def description(self, description: str or Literal):
        if type(description) is str:
            self._description = description
        elif type(description) is Literal:
            self._description = str(description)
        else:
            raise TypeError

        self._rdf.add(
            (self._iri, DCTERMS.description, Literal(self._description))
        )

        self._tainted = True

    @property
    def issued(self):
        """The ``dcterms:issued`` property."""
        return self._issued

    @issued.setter
    def issued(self, issued: datetime.datetime or str):
        if type(issued) is datetime.datetime:
            self._issued = issued
        elif type(issued) is str:
            self._issued = datetime.datetime.fromisoformat(issued)
        else:
            raise TypeError(
                (
                    "issue property must be a datetime.datetime "
                    "class instance or a string in the "
                    'format"YYYY-MM-DDTHH:MM:SSTZ".'
                )
            )

        self._rdf.add((self._iri, DCTERMS.issued, Literal(self._issued)))

        self._tainted = True

    @property
    def license(self):
        """The ``dcterms:license`` property.

        .. note::
            must follow recommendation from:
            https://joinup.ec.europa.eu/release/dcat-ap-how-refer-licence-documents-and-licence-uris
        """
        return self._license

    @license.setter
    def license(self, license_uri: str):
        if type(license_uri) is str:
            self._license = license_uri
        elif type(license_uri) is URIRef:
            self._license = str(license_uri)
        else:
            raise TypeError(
                (
                    "license property must be an URIRef "
                    "class instance or a str."
                )
            )

        self._rdf.add((self._iri, DCTERMS.license, URIRef(self._license)))

        self._tainted = True

    @property
    def publisher(self):
        """The ``dcterms:publisher`` property."""
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str or dict or fdp.foaf.FOAFAgent):
        if isinstance(publisher, str):
            self._publisher = fdp.foaf.FOAFAgent()
            self._publisher.name = publisher

            self._rdf += self._publisher.rdf

            self._tainted = True
        elif isinstance(publisher, fdp.foaf.FOAFAgent):
            self._publisher = publisher

            self._rdf += self._publisher.rdf

            self._tainted = True
        else:
            raise TypeError(
                (
                    "publisher must be a FOAFAgent's class instance "
                    "or a string."
                )
            )

        self._rdf.add((self._iri, DCTERMS.publisher, self._publisher.iri))

    @property
    def theme(self):
        """The ``dcat:theme`` property.

        .. note::
            a list of themes can be found here:
            https://inspire.ec.europa.eu/theme
        """
        return self._theme

    @theme.setter
    def theme(self, theme_uri: str):
        if type(theme_uri) is str:
            self._theme = theme_uri
        elif type(theme_uri) is URIRef:
            self._theme = str(theme_uri)
        else:
            raise TypeError(
                ("theme property must be an URIRef " "class instance or a str.")
            )

        self._rdf.add((self._iri, DCAT.theme, URIRef(self._theme)))

        self._tainted = True

    @property
    def title(self):
        """The ``dcterms:title`` property."""
        return self._title

    @title.setter
    def title(self, title: str or Literal):
        if type(title) is str:
            self._title = title
        elif type(title) is Literal:
            self._title = str(title)
        else:
            raise TypeError

        self._rdf.add((self._iri, DCTERMS.title, Literal(self._title)))

        self._tainted = True

    @property
    def version(self):
        """The ``dcat:version`` property."""
        return self._version

    @version.setter
    def version(
        self, version: str or fdp.version.Version or int or tuple(int, int, int)
    ):
        if type(version) is str:
            self._version = fdp.version.Version(version=version)
        elif type(version) is tuple:
            self._version = fdp.version.Version(version=version)
        elif type(version) is fdp.version.Version:
            self._version = version
        elif type(version) is int:
            self._version = fdp.version.Version(major=version, minor=0, patch=0)
        else:
            raise TypeError("version must be a Version's class valid value.")
        self._rdf.add(
            (self._iri, DCAT.version, Literal(self._version.as_str()))
        )

        self._tainted = True

    @property
    def rdf(self) -> str:
        """The rdf graph of the Resource instance."""
        return self._rdf

    def _content(self):
        return self._rdf.serialize(format="turtle")
