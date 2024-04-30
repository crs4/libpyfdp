# pylint: disable=unidiomatic-typecheck,missing-module-docstring

import pytest
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import XSD, Namespace
# import uuid

from fdp.distribution import Distribution, Checksum

SPDX = Namespace("http://spdx.org/rdf/terms")


class TestDistribution:
    """Unit test for the Distribution DCAT class."""
    license_url = 'https://creativecommons.org/publicdomain/zero/1.0/'
    download_url = "https://www.example.com/downloads/file.tar.gz"
    byte_size = 1024
    media_type = ('http://www.iana.org/assignments/media-types/'
                  'text/tab-separated-values')
    compress_format = ("http://www.iana.org/assignments/media-types/"
                       "application/gzip")

    ###########################################################################
    def test_distribution_set_iri(self):
        """Checks the Distribution's IRI setter/getter."""

        # Property not set
        distribution = Distribution(iri=None)
        assert type(distribution.iri) is BNode

#         # Property set as a str
#         distribution = Distribution(iri='A string IRI')
#         assert type(distribution.iri) is URIRef
#         assert distribution.iri == URIRef('A string IRI')
#
#         # Property set as a URIRef
#         distribution = Distribution(iri=URIRef('A string IRI'))
#         assert type(distribution.iri) is URIRef
#         assert distribution.iri == URIRef('A string IRI')
#
#         # Property set as a BNode
#         distribution = Distribution(iri=BNode())
#         assert type(distribution.iri) is BNode
#
#         # Property set as a UUID
#         _uuid = uuid.uuid1()
#         distribution = Distribution(uuid=_uuid)
#         assert type(distribution.iri) is URIRef
#         assert distribution.iri ==
#         URIRef(f'http://127.0.0.1/distribution/{_uuid}')

    def test_distribution_download_url_property(self):
        """Checks the Distribution's downloadURL property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.downloadURL is None
        assert distribution.tainted is False

        # Property set as a str
        distribution = Distribution()
        distribution.downloadURL = self.download_url
        assert type(distribution.downloadURL) is str
        assert distribution.downloadURL == self.download_url
        assert distribution.tainted is True

        # Property set as a Literal
        distribution = Distribution()
        distribution.downloadURL = Literal(self.download_url)
        assert type(distribution.downloadURL) is str
        assert distribution.downloadURL == self.download_url

        # Property set as an incompatible data type
        distribution = Distribution()

        with pytest.raises(TypeError):
            distribution.downloadURL = 15
        assert distribution.downloadURL is None
        assert distribution.tainted is False

    def test_distribution_byte_size_property(self):
        """Checks the Distribution's byteSize property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.byteSize is None
        assert distribution.tainted is False

        # Property set as a int
        distribution = Distribution()
        distribution.byteSize = self.byte_size
        assert type(distribution.byteSize) is int
        assert distribution.byteSize == self.byte_size
        assert distribution.tainted is True

        # Property set as a Literal
        distribution = Distribution()
        distribution.byteSize = Literal(self.byte_size,
                                        datatype=XSD.nonNegativeInteger)
        assert type(distribution.byteSize) is int
        assert distribution.byteSize == self.byte_size

        # Property set as an incompatible data type
        distribution = Distribution()

        with pytest.raises(TypeError):
            distribution.byteSize = "a string"
        assert distribution.byteSize is None
        assert distribution.tainted is False

    def test_distribution_compress_format_property(self):
        """Checks the Distribution's compressFormat property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.compressFormat is None
        assert distribution.tainted is False

        # Property set as a str
        distribution = Distribution()
        distribution.compressFormat = self.compress_format
        assert type(distribution.compressFormat) is str
        assert distribution.compressFormat == self.compress_format
        assert distribution.tainted is True

        # Property set as an URIRef
        distribution = Distribution()
        distribution.compressFormat = URIRef(self.compress_format)
        assert type(distribution.compressFormat) is str
        assert distribution.compressFormat == self.compress_format
        assert distribution.tainted is True

        # Property set as an incompatible data type
        distribution = Distribution()

        with pytest.raises(TypeError):
            distribution.compressFormat = 15
        assert distribution.compressFormat is None
        assert distribution.tainted is False

    def test_distribution_license_property(self):
        """Checks the Distribution's license property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.license is None
        assert distribution.tainted is False

        # Property set as a str
        distribution = Distribution()
        distribution.license = self.license_url
        assert type(distribution.license) is str
        assert distribution.license == self.license_url
        assert distribution.tainted is True

        # Property set as an URIRef
        distribution = Distribution()
        distribution.license = URIRef(self.license_url)
        assert type(distribution.license) is str
        assert distribution.license == self.license_url
        assert distribution.tainted is True

        # Property set as an incompatible data type
        distribution = Distribution()

        with pytest.raises(TypeError):
            distribution.license = 15
        assert distribution.license is None
        assert distribution.tainted is False

    def test_distribution_media_type_property(self):
        """Checks the Distribution's mediaType property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.mediaType is None
        assert distribution.tainted is False

        # Property set as a str
        distribution = Distribution()
        distribution.mediaType = self.media_type
        assert type(distribution.mediaType) is str
        assert distribution.mediaType == self.media_type
        assert distribution.tainted is True

        # Property set as an URIRef
        distribution = Distribution()
        distribution.mediaType = URIRef(self.media_type)
        assert type(distribution.mediaType) is str
        assert distribution.mediaType == self.media_type
        assert distribution.tainted is True

        # Property set as an incompatible data type
        distribution = Distribution()

        with pytest.raises(TypeError):
            distribution.mediaType = 15
        assert distribution.mediaType is None
        assert distribution.tainted is False

    def test_distribution_checksum_property(self):
        """Checks the Distribution's checksum property setter/getter."""

        # Property not set
        distribution = Distribution()
        assert distribution.checksum is None
        assert distribution.tainted is False

        # # Property set as a str
        # distribution = Distribution()
        # distribution.checksum = self.media_type
        # assert type(distribution.checksum) is str
        # assert distribution.checksum == self.media_type
        # assert distribution.tainted is True

        # # Property set as an URIRef
        # distribution = Distribution()
        # distribution.checksum = URIRef(self.media_type)
        # assert type(distribution.checksum) is str
        # assert distribution.checksum == self.media_type
        # assert distribution.tainted is True

        # # Property set as an incompatible data type
        # distribution = Distribution()

        # with pytest.raises(TypeError):
        #     distribution.checksum = 15
        # assert distribution.checksum is None
        # assert distribution.tainted is False


class TestChecksum:
    """Unit test for the Checksum DCATv3 class."""
    algorithm_uriref = SPDX.checksumAlgorithm_md5
    algorithm_str = "SPDX.checksumAlgorithm_md5"
    checksumValue = "9dd39a0cb943e5d33d5a044bad6030a4"

    ###########################################################################
    def test_checksum_set_iri(self):
        """Checks the Checksum's IRI setter/getter."""

        # Property not set
        checksum = Checksum(iri=None)
        assert type(checksum.iri) is BNode

#         # Property set as a str
#         checksum = Checksum(iri='A string IRI')
#         assert type(checksum.iri) is URIRef
#         assert checksum.iri == URIRef('A string IRI')
#
#         # Property set as a URIRef
#         checksum = Checksum(iri=URIRef('A string IRI'))
#         assert type(checksum.iri) is URIRef
#         assert checksum.iri == URIRef('A string IRI')
#
#         # Property set as a BNode
#         checksum = Checksum(iri=BNode())
#         assert type(checksum.iri) is BNode
#
#         # Property set as a UUID
#         _uuid = uuid.uuid1()
#         checksum = Checksum(uuid=_uuid)
#         assert type(checksum.iri) is URIRef
#         assert checksum.iri ==
#         URIRef(f'http://127.0.0.1/checksum/{_uuid}')

    def test_checksum_algorithm_property(self):
        """Checks the Checksum's algorithm property setter/getter."""

        # Property not set
        checksum = Checksum()
        assert checksum.algorithm is None
        assert checksum.tainted is False

        # Property set as a str
        checksum = Checksum()
        checksum.algorithm = self.algorithm_str
        assert type(checksum.algorithm) is str
        assert checksum.algorithm == self.algorithm_str
        assert checksum.tainted is True

        # Property set as a URIRef
        checksum = Checksum()
        checksum.algorithm = self.algorithm_uriref
        assert type(checksum.algorithm) is str
        assert checksum.algorithm == str(self.algorithm_uriref)
        assert checksum.tainted is True

        # Property set as an incompatible data type
        checksum = Checksum()

        with pytest.raises(TypeError):
            checksum.algorithm = 15
        assert checksum.algorithm is None
        assert checksum.tainted is False

    def test_checksum_value_property(self):
        """Checks the Checksum's checksumValue property setter/getter."""

        # Property not set
        checksum = Checksum()
        assert checksum.checksumValue is None
        assert checksum.tainted is False

        # Property set as a str
        checksum = Checksum()
        checksum.checksumValue = self.checksumValue
        assert type(checksum.checksumValue) is str
        assert checksum.checksumValue == self.checksumValue
        assert checksum.tainted is True

        # Property set as a Literal
        checksum = Checksum()
        checksum.checksumValue = Literal(self.checksumValue,
                                         datatype=XSD.hexBinary)
        assert type(checksum.checksumValue) is str
        assert checksum.checksumValue == self.checksumValue
        assert checksum.tainted is True

        # Property set as an incompatible data type
        checksum = Checksum()

        with pytest.raises(TypeError):
            checksum.checksumValue = 15
        assert checksum.checksumValue is None
        assert checksum.tainted is False

        checksum = Checksum()

        with pytest.raises(TypeError):
            checksum.checksumValue = Literal(self.checksumValue,
                                             datatype=XSD.string)
        assert checksum.checksumValue is None
        assert checksum.tainted is False
