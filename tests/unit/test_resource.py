# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
import datetime
import uuid

import pytest

from rdflib import Literal, URIRef, BNode

import fdp
from fdp.resource import Resource
from fdp.foaf import FOAFAgent, FOAFPerson, FOAFOrganization, FOAFGroup


class TestResource:
    version_tuple = (1, 0, 0)
    version_string = '1.0.0'
    license_url = 'https://creativecommons.org/publicdomain/zero/1.0/'
    theme_url = 'https://inspire.ec.europa.eu/theme/pf'

    ###########################################################################
    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return Resource

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_set_iri(self, testing_class):
        """Checks the Resource's IRI setter/getter."""

        # Property not set
        resource = testing_class(iri=None)
        assert type(resource.iri) is BNode

        # Property set as a str
        resource = testing_class(iri='A string IRI')
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef('A string IRI')

        # Property set as a URIRef
        resource = testing_class(iri=URIRef('A string IRI'))
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef('A string IRI')

        # Property set as a BNode
        resource = testing_class(iri=BNode())
        assert type(resource.iri) is BNode

        # Property set as a UUID
        _uuid = uuid.uuid1()
        resource = testing_class(uuid=_uuid)
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef(
            f'http://127.0.0.1/{testing_class.URL_PATH}/{_uuid}')

    def test_set_creator_property(self, testing_class):
        """Checks the Resource's creator property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.creator is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.creator = "A Creator"
        assert type(resource.creator) is FOAFAgent
        assert resource.creator.name == "A Creator"
        assert resource.tainted is True

        # Property set as a Group
        resource = testing_class()
        resource.creator = FOAFGroup()
        resource.creator.name = "A Creator Group"
        resource.creator.homepage = "A Creator Group Homepage"
        assert resource.creator.member is None

        resource.creator.add_member(FOAFPerson(name="A Creator Member"))
        assert type(resource.creator) is FOAFGroup
        assert resource.creator.name == "A Creator Group"
        assert resource.creator.homepage == ("A Creator Group "
                                             "Homepage")
        assert len(resource.creator.member) == 1
        for _iri, _member in resource.creator.member.items():
            assert type(_member) is FOAFPerson
            assert _member.name == "A Creator Member"

        assert resource.tainted is True

        # Property set as an Organization
        resource = testing_class()
        resource.creator = FOAFOrganization()
        resource.creator.name = "A Creator Organization"
        resource.creator.homepage = "A Creator Organization Homepage"
        assert resource.creator.name == "A Creator Organization"
        assert resource.creator.homepage == ("A Creator Organization "
                                             "Homepage")

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.creator = 15
        assert resource.creator is None
        assert resource.tainted is False

    def test_set_description_property(self, testing_class):
        """Checks the Resource's description property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.description is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.description = 'A string description'
        assert type(resource.description) is str
        assert resource.description == 'A string description'
        assert resource.tainted is True

        # Property set as a Literal
        resource = testing_class()
        resource.description = Literal('A string description')
        assert type(resource.description) is str
        assert resource.description == 'A string description'
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.description = 15
        assert resource.tainted is False

    def test_set_issued_property(self, testing_class):
        """Checks the Resource's issued property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.issued is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.issued = '2024-04-03'
        assert type(resource.issued) is datetime.datetime
        assert resource.issued == datetime.datetime.fromisoformat('2024-04-03')
        assert resource.tainted is True

        # Property set as a datetime
        resource = testing_class()
        resource.issued = datetime.datetime.fromisoformat('2024-04-03')
        assert type(resource.issued) is datetime.datetime
        assert resource.issued == datetime.datetime.fromisoformat('2024-04-03')
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.issued = 15
        assert resource.issued is None
        assert resource.tainted is False

    def test_set_license_property(self, testing_class):
        """Checks the Resource's license property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.license is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.license = self.license_url
        assert type(resource.license) is str
        assert resource.license == self.license_url
        assert resource.tainted is True

        # Property set as an URIRef
        resource = testing_class()
        resource.license = URIRef(self.license_url)
        assert type(resource.license) is str
        assert resource.license == self.license_url
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.license = 15
        assert resource.license is None
        assert resource.tainted is False

    def test_set_publisher_property(self, testing_class):
        """Checks the Resource's publisher property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.publisher is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.publisher = "A Publisher"
        assert type(resource.publisher) is FOAFAgent
        assert resource.publisher.name == "A Publisher"
        assert resource.tainted is True

        # Property set as a Group
        resource = testing_class()
        resource.publisher = FOAFGroup()
        resource.publisher.name = "A Publisher Group"
        resource.publisher.homepage = "A Publisher Group Homepage"
        assert resource.publisher.member is None

        resource.publisher.add_member(FOAFPerson(name="A Publisher Member"))
        assert type(resource.publisher) is FOAFGroup
        assert resource.publisher.name == "A Publisher Group"
        assert resource.publisher.homepage == ("A Publisher Group "
                                               "Homepage")
        assert len(resource.publisher.member) == 1
        for _iri, _member in resource.publisher.member.items():
            assert type(_member) is FOAFPerson
            assert _member.name == "A Publisher Member"

        assert resource.tainted is True

        # Property set as an Organization
        resource = testing_class()
        resource.publisher = FOAFOrganization()
        resource.publisher.name = "A Publisher Organization"
        resource.publisher.homepage = "A Publisher Organization Homepage"
        assert resource.publisher.name == "A Publisher Organization"
        assert resource.publisher.homepage == ("A Publisher Organization "
                                               "Homepage")

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.publisher = 15
        assert resource.publisher is None
        assert resource.tainted is False

    def test_set_theme_property(self, testing_class):
        """Checks the Resource's theme property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.theme is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.theme = self.theme_url
        assert type(resource.theme) is str
        assert resource.theme == self.theme_url
        assert resource.tainted is True

        # Property set as an URIRef
        resource = testing_class()
        resource.theme = URIRef(self.theme_url)
        assert type(resource.theme) is str
        assert resource.theme == self.theme_url
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = testing_class()

        with pytest.raises(TypeError):
            resource.theme = 15
        assert resource.theme is None
        assert resource.tainted is False

    def test_set_title_property(self, testing_class):
        """Checks the Resource's title property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.title is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.title = 'A string title'
        assert type(resource.title) is str
        assert resource.title == 'A string title'
        assert resource.tainted is True

        # Property set as a Literal
        resource = testing_class()
        resource.title = Literal('A string title')
        assert type(resource.title) is str
        assert resource.title == 'A string title'
        assert resource.tainted is True

        resource = testing_class()

        # Property set as an incompatible data type
        with pytest.raises(TypeError):
            resource.title = 15
        assert resource.tainted is False

    def test_set_version_property(self, testing_class):
        """Checks the Resource's version property setter/getter."""

        # Property not set
        resource = testing_class()
        assert resource.version is None
        assert resource.tainted is False

        # Property set as a str
        resource = testing_class()
        resource.version = self.version_string
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_string)
        assert resource.tainted is True

        # Property set as a Tuple
        resource = testing_class()
        resource.version = self.version_tuple
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_tuple)
        assert resource.tainted is True

        # Property set as a Version
        resource = testing_class()
        resource.version = fdp.version.Version(self.version_string)
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_string)
        assert resource.tainted is True

        # Property set as a single int
        resource = testing_class()

        resource.version = 15
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version((15, 0, 0))
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = testing_class()
        with pytest.raises(TypeError):
            resource.version = [1, 2, 3]
        assert resource.tainted is False

        # Property set with setter/getter/reset
        resource = testing_class()

        resource.version = fdp.version.Version()

        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version((1, 0, 0))
        assert resource.tainted is True

        resource.version.major = 10
        resource.version.minor = 20
        resource.version.patch = 30

        assert resource.version == fdp.version.Version((10, 20, 30))

        resource.version.reset()
        assert resource.version == fdp.version.Version((1, 0, 0))
        assert resource.tainted is True
