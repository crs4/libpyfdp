# pylint: disable=unidiomatic-typecheck,invalid-name,missing-module-docstring
# pylint: disable=too-many-instance-attributes

from rdflib import URIRef, Literal, Graph, BNode
from rdflib.namespace import DCTERMS, DCAT, XSD, RDF, Namespace

import fdp.fairdatapoint

SPDX = Namespace("http://spdx.org/rdf/terms#")


class Checksum():
    """Class representing a DCATv3 package checksum."""

    _CHECKSUM_PROPERTIES = ['algorithm', 'checksumValue']

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        for _p in self._CHECKSUM_PROPERTIES:
            setattr(Checksum, f'_{_p}', None)

        self._rdf = Graph()
        self._rdf.bind("spdx", SPDX)

        self._uuid = uuid

        if iri is not None:
            # if type(iri) is str:
            #     self._iri = URIRef(iri)
            # elif type(iri) in [IdentifiedNode, URIRef, BNode]:
            #     self._iri = iri
            # else:
            raise TypeError((f'Type {type(iri)} not allowed for '
                             '"iri" argument'))
        # elif self._uuid is not None:
        #     self._iri = URIRef(
        #         f'{self._fair_data_point}/resource/{self._uuid}')
        # # XXX Check this
        # dataset_serie_distribution_iri = dataset_serie_iri + URIRef(
        #     f"/distribution/{house_name}.zip")
        else:
            self._iri = BNode()

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            SPDX.Checksum))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the Checksum instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the Checksum instance."""
        return self._rdf

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def algorithm(self):
        """The ``spdx:algorithm`` property of the Checksum's instance."""
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: str):
        if type(algorithm) is str:
            self._algorithm = algorithm
        elif type(algorithm) is URIRef:
            self._algorithm = str(algorithm)
        else:
            raise TypeError("algorithm property must be a str or a URIRef.")

        self._rdf.add((
            self._iri,
            SPDX.algorithm,
            URIRef(self._algorithm)))

        self._tainted = True

    @property
    def checksumValue(self):
        """ The ``spdx:checksumValue`` property."""
        return self._checksumValue

    @checksumValue.setter
    def checksumValue(self, checksumValue: str or Literal):
        if type(checksumValue) is str:
            self._checksumValue = checksumValue
        elif (type(checksumValue) is Literal and
              checksumValue.datatype == XSD.hexBinary):
            self._checksumValue = str(checksumValue)
        else:
            raise TypeError("checksumValue property must be a str or a "
                            "Literal of type xsd:hexBinary.")

        self._rdf.add((
            self._iri,
            SPDX.checksumValue,
            Literal(self._checksumValue,
                    datatype=XSD.hexBinary)
        ))

        self._tainted = True


class Distribution():
    """Class representing a DCATv3 dcat:Distribution.

    dcat:Distribution represents an accessible form of a dataset such as a
    downloadable file.
    """

    _DISTRIBUTION_PROPERTIES = ['checksum', 'downloadURL', 'license',
                                'mediaType', 'compressFormat', 'byteSize']

    __frozen = False

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 iri: str = None, uuid: str = None):
        for _p in self._DISTRIBUTION_PROPERTIES:
            setattr(Distribution, f'_{_p}', None)

        self._rdf = Graph()

        self._rdf.bind("dcat", DCAT)
        self._rdf.bind("dcterms", DCTERMS)
        self._rdf.bind("spdx", SPDX)

        self._uuid = uuid
        self._fair_data_point = fair_data_point or 'http://127.0.0.1'

        if iri is not None:
            # if type(iri) is str:
            #     self._iri = URIRef(iri)
            # elif type(iri) in [IdentifiedNode, URIRef, BNode]:
            #     self._iri = iri
            # else:
            raise TypeError((f'Type {type(iri)} not allowed for '
                             '"iri" argument'))
        # elif self._uuid is not None:
        #     self._iri = URIRef(
        #         f'{self._fair_data_point}/resource/{self._uuid}')
        # # XXX Check this
        # dataset_serie_distribution_iri = dataset_serie_iri + URIRef(
        #     f"/distribution/{house_name}.zip")
        else:
            self._iri = BNode()

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            DCAT.Distribution))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the Distribution instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the Distribution instance."""
        return self._rdf

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def downloadURL(self):
        """The ``dcat:downloadURL`` property."""
        return self._downloadURL

    @downloadURL.setter
    def downloadURL(self, downloadURL: str or URIRef):
        if type(downloadURL) is str:
            self._downloadURL = downloadURL
        elif type(downloadURL) is URIRef:
            self._downloadURL = str(downloadURL)
        else:
            raise TypeError("downloadURL property must be a str or a URIRef.")

        self._rdf.add((
            self._iri,
            DCAT.downloadURL,
            URIRef(self._downloadURL)))

        self._tainted = True

    @property
    def byteSize(self):
        """ The ``dcat:byteSize`` property."""
        return self._byteSize

    @byteSize.setter
    def byteSize(self, byteSize: int):
        if type(byteSize) is int:
            self._byteSize = byteSize
        elif type(byteSize) is Literal:
            self._byteSize = int(byteSize)
        else:
            raise TypeError("byteSize property must be an int.")

        self._rdf.add((
            self._iri,
            DCAT.byteSize,
            Literal(self._byteSize,
                    datatype=XSD.nonNegativeInteger)))

        self._tainted = True

    @property
    def license(self):
        """ The ``dcterms:license`` property.

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
            raise TypeError(("license property must be an URIRef "
                             "class instance or a str."))

        self._rdf.add((
            self._iri,
            DCTERMS.license,
            Literal(self._license)
        ))

        self._tainted = True

    @property
    def mediaType(self):
        """The ``dcat:mediaType`` property."""
        return self._mediaType

    @mediaType.setter
    def mediaType(self, mediaType: str or URIRef):
        if type(mediaType) is str:
            self._mediaType = mediaType
        elif type(mediaType) is URIRef:
            self._mediaType = str(mediaType)
        else:
            raise TypeError(("mediaType property must be a str or a "
                             "URIRef class instance."))

        self._rdf.add((
            self._iri,
            DCAT.mediaType,
            URIRef(self._mediaType)))

        self._tainted = True

    @property
    def compressFormat(self):
        """The ``dcat:compressFormat`` property."""
        return self._compressFormat

    @compressFormat.setter
    def compressFormat(self, compressFormat: str or URIRef):
        if type(compressFormat) is str:
            self._compressFormat = compressFormat
        elif type(compressFormat) is URIRef:
            self._compressFormat = str(compressFormat)
        else:
            raise TypeError(("compressFormat property must be a str or a "
                             "URIRef class instance."))

        self._rdf.add((
            self._iri,
            DCAT.compressFormat,
            URIRef(self._compressFormat)
        ))

        self._tainted = True

    @property
    def checksum(self):
        """The ``dcat:checksum`` property."""
        return self._checksum

    @checksum.setter
    def checksum(self, checksum: Checksum):
        if type(checksum) is Checksum:
            self._checksum = checksum
        else:
            raise TypeError(("checksum property must be a Checksum "
                             "class instance."))

        self._rdf += self._checksum.rdf

        self._rdf.add((
            self._iri,
            DCAT.checksum,
            self._checksum.iri
        ))

        self._tainted = True
