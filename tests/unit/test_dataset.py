# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
import datetime

import pytest

from rdflib import BNode, IdentifiedNode, URIRef
from rdflib.namespace import Namespace


from fdp.dataset import Dataset, DatasetSeries
from fdp.distribution import Distribution, Checksum
from fdp.foaf import FOAFGroup, FOAFOrganization, FOAFPerson

from test_resource import TestResource

SPDX = Namespace("http://spdx.org/rdf/terms")


@pytest.fixture(scope="session")
def tsv_distribution():
    """Returns a TSV compressed file Distribution."""

    distribution = Distribution()
    distribution.downloadURL = "https://www.example.com/downloads/file.tar.gz"
    distribution.license = 'https://creativecommons.org/publicdomain/zero/1.0/'
    distribution.mediaType = ('http://www.iana.org/assignments/media-types/'
                              'text/tab-separated-values')
    distribution.compressFormat = ("http://www.iana.org/assignments/"
                                   "media-types/application/gzip")
    distribution.byteSize = 1024

    distribution.checksum = Checksum()
    distribution.checksum.algorithm = SPDX.checksumAlgorithm_md5
    distribution.checksum.checksumValue = "9dd39a0cb943e5d33d5a044bad6030a4"

    return distribution


@pytest.fixture(scope="class")
def csv_distribution():
    """Returns a TSV compressed file Distribution."""

    distribution = Distribution()
    distribution.downloadURL = "https://www.example.com/downloads/file.zip"
    distribution.license = 'https://creativecommons.org/publicdomain/zero/1.0/'
    distribution.mediaType = ('http://www.iana.org/assignments/media-types/'
                              'text/comma-separated-values')
    distribution.compressFormat = ("http://www.iana.org/assignments/"
                                   "media-types/application/zip")
    distribution.byteSize = 2048

    distribution.checksum = Checksum()
    distribution.checksum.algorithm = SPDX.checksumAlgorithm_md5
    distribution.checksum.checksumValue = "9dd39a0cb943e5d33d5a044bad6030a4"

    return distribution


@pytest.fixture(scope="class")
def dataset_series(csv_distribution):
    """Returns a DatasetSeries."""

    dataset_series = DatasetSeries()
    dataset_series.title = "A Dataset Series"
    dataset_series.license = ("https://creativecommons.org/publicdomain/"
                              "zero/1.0/")
    dataset_series.version = "1.0.0"
    dataset_series.issued = datetime.datetime(1970, 1, 1)

    dataset_serie_publisher = FOAFOrganization()
    dataset_serie_publisher.name = "A Publisher Organization"
    dataset_serie_publisher.homepage = "http://www.example.com/"
    dataset_series.publisher = dataset_serie_publisher

    dataset_serie_creator = FOAFGroup()
    author = FOAFPerson()
    author.name = "An Author"
    dataset_serie_creator.add_member(author)
    dataset_series.creator = dataset_serie_creator

    dataset_series.add_distribution(csv_distribution)

    return dataset_series


class TestDataset(TestResource):
    """Test case for the Dataset class."""

    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return Dataset

    def test_dataset_add_distribution(self, tsv_distribution,
                                      csv_distribution, testing_class):
        """Tests the distribution property's setter/getter."""

        dataset = testing_class()
        dataset.add_distribution(tsv_distribution)

        assert len(dataset.distribution) == 1

        dataset.add_distribution(csv_distribution)

        assert len(dataset.distribution) == 2

        # check duplications
        dataset.add_distribution(csv_distribution)

        assert len(dataset.distribution) == 2

        for distro_iri, distro_obj in dataset.distribution.items():
            assert distro_iri in [tsv_distribution.iri, csv_distribution.iri]
            assert type(distro_obj) is Distribution

        # Property set as an incompatible data type
        dataset = testing_class()

        with pytest.raises(TypeError):
            dataset.add_distribution("A string distribution?")

        assert dataset.creator is None
        assert dataset.tainted is False

    def test_dataset_in_series(self, dataset_series, testing_class):
        """Tests the inSeries property's setter/getter."""

        dataset = testing_class()

        assert dataset.inSeries is None
        assert dataset.tainted is False

        # Property set as a str
        dataset = testing_class()
        dataset.inSeries = str(dataset_series.iri)

        assert isinstance(dataset.inSeries, URIRef) is True
        assert isinstance(dataset.inSeries, IdentifiedNode) is True
        assert dataset.tainted is True

        # Property set as a BNode
        dataset = testing_class()
        dataset.inSeries = BNode()

        assert isinstance(dataset.inSeries, BNode) is True
        assert isinstance(dataset.inSeries, IdentifiedNode) is True
        assert dataset.tainted is True

        # Property set as a URIRef
        dataset = testing_class()
        dataset.inSeries = URIRef(str(dataset_series.iri))

        assert isinstance(dataset.inSeries, URIRef) is True
        assert isinstance(dataset.inSeries, IdentifiedNode) is True
        assert dataset.tainted is True

        # Property set as an incompatible data type
        dataset = testing_class()

        with pytest.raises(TypeError):
            dataset.inSeries = 15

        assert dataset.inSeries is None
        assert dataset.tainted is False
