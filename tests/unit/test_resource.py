import datetime
import pytest
from rdflib import Literal, URIRef, BNode
import uuid

import fdp
from fdp.resource import Resource
from fdp.foaf import FOAFAgent, FOAFPerson, FOAFOrganization, FOAFGroup


class TestResource:
    version_tuple = (1, 0, 0)
    version_string = '1.0.0'
    license_url = 'https://creativecommons.org/publicdomain/zero/1.0/'

    ###########################################################################
    def test_resource_set_iri(self):
        """Checks the Resource's IRI setter/getter."""

        # Property not set
        resource = Resource(iri=None)
        assert type(resource.iri) is BNode

        # Property set as a str
        resource = Resource(iri='A string IRI')
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef('A string IRI')

        # Property set as a URIRef
        resource = Resource(iri=URIRef('A string IRI'))
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef('A string IRI')

        # Property set as a BNode
        resource = Resource(iri=BNode())
        assert type(resource.iri) is BNode

        # Property set as a UUID
        _uuid = uuid.uuid1()
        resource = Resource(uuid=_uuid)
        assert type(resource.iri) is URIRef
        assert resource.iri == URIRef(f'http://127.0.0.1/resource/{_uuid}')

    def test_resource_set_creator_property(self):
        """Checks the Resource's creator property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.creator is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.creator = "A Creator"
        assert type(resource.creator) is FOAFAgent
        assert resource.creator.name == "A Creator"
        assert resource.tainted is True

        # Property set as a Group
        resource = Resource()
        resource.creator = FOAFGroup()
        resource.creator.name = "A Creator Group"
        resource.creator.homepage = "A Creator Group Homepage"
        assert len(resource.creator.members) == 0

        resource.creator.add_member(FOAFPerson(name="A Creator Member"))
        assert type(resource.creator) is FOAFGroup
        assert resource.creator.name == "A Creator Group"
        assert resource.creator.homepage == ("A Creator Group "
                                             "Homepage")
        assert len(resource.creator.members) == 1
        for _iri, _member in resource.creator.members.items():
            assert type(_member) is FOAFPerson
            assert _member.name == "A Creator Member"

        assert resource.tainted is True

        # Property set as an Organization
        resource = Resource()
        resource.creator = FOAFOrganization()
        resource.creator.name = "A Creator Organization"
        resource.creator.homepage = "A Creator Organization Homepage"
        assert resource.creator.name == "A Creator Organization"
        assert resource.creator.homepage == ("A Creator Organization "
                                             "Homepage")

        # Property set as an incompatible data type
        resource = Resource()

        with pytest.raises(TypeError):
            resource.creator = 15
        assert resource.creator is None
        assert resource.tainted is False

    def test_resource_set_description_property(self):
        """Checks the Resource's description property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.description is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.description = 'A string description'
        assert type(resource.description) is str
        assert resource.description == 'A string description'
        assert resource.tainted is True

        # Property set as a Literal
        resource = Resource()
        resource.description = Literal('A string description')
        assert type(resource.description) is str
        assert resource.description == 'A string description'
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = Resource()

        with pytest.raises(TypeError):
            resource.description = 15
        assert resource.tainted is False

    def test_resource_set_issued_property(self):
        """Checks the Resource's issued property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.issued is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.issued = '2024-04-03'
        assert type(resource.issued) is datetime.datetime
        assert resource.issued == datetime.datetime.fromisoformat('2024-04-03')
        assert resource.tainted is True

        # Property set as a datetime
        resource = Resource()
        resource.issued = datetime.datetime.fromisoformat('2024-04-03')
        assert type(resource.issued) is datetime.datetime
        assert resource.issued == datetime.datetime.fromisoformat('2024-04-03')
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = Resource()

        with pytest.raises(TypeError):
            resource.issued = 15
        assert resource.issued is None
        assert resource.tainted is False

    def test_resource_set_license_property(self):
        """Checks the Resource's license property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.license is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.license = self.license_url
        assert type(resource.license) is str
        assert resource.license == self.license_url
        assert resource.tainted is True

        # Property set as an URIRef
        resource = Resource()
        resource.license = URIRef(self.license_url)
        assert type(resource.license) is str
        assert resource.license == self.license_url
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = Resource()

        with pytest.raises(TypeError):
            resource.license = 15
        assert resource.license is None
        assert resource.tainted is False

    def test_resource_set_publisher_property(self):
        """Checks the Resource's publisher property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.publisher is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.publisher = "A Publisher"
        assert type(resource.publisher) is FOAFAgent
        assert resource.publisher.name == "A Publisher"
        assert resource.tainted is True

        # Property set as a Group
        resource = Resource()
        resource.publisher = FOAFGroup()
        resource.publisher.name = "A Publisher Group"
        resource.publisher.homepage = "A Publisher Group Homepage"
        assert len(resource.publisher.members) == 0

        resource.publisher.add_member(FOAFPerson(name="A Publisher Member"))
        assert type(resource.publisher) is FOAFGroup
        assert resource.publisher.name == "A Publisher Group"
        assert resource.publisher.homepage == ("A Publisher Group "
                                               "Homepage")
        assert len(resource.publisher.members) == 1
        for _iri, _member in resource.publisher.members.items():
            assert type(_member) is FOAFPerson
            assert _member.name == "A Publisher Member"

        assert resource.tainted is True

        # Property set as an Organization
        resource = Resource()
        resource.publisher = FOAFOrganization()
        resource.publisher.name = "A Publisher Organization"
        resource.publisher.homepage = "A Publisher Organization Homepage"
        assert resource.publisher.name == "A Publisher Organization"
        assert resource.publisher.homepage == ("A Publisher Organization "
                                               "Homepage")

        # Property set as an incompatible data type
        resource = Resource()

        with pytest.raises(TypeError):
            resource.publisher = 15
        assert resource.publisher is None
        assert resource.tainted is False

    def test_resource_set_title_property(self):
        """Checks the Resource's title property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.title is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.title = 'A string title'
        assert type(resource.title) is str
        assert resource.title == 'A string title'
        assert resource.tainted is True

        # Property set as a Literal
        resource = Resource()
        resource.title = Literal('A string title')
        assert type(resource.title) is str
        assert resource.title == 'A string title'
        assert resource.tainted is True

        resource = Resource()

        # Property set as an incompatible data type
        with pytest.raises(TypeError):
            resource.title = 15
        assert resource.tainted is False

    def test_resource_set_version_property(self):
        """Checks the Resource's version property setter/getter."""

        # Property not set
        resource = Resource()
        assert resource.version is None
        assert resource.tainted is False

        # Property set as a str
        resource = Resource()
        resource.version = self.version_string
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_string)
        assert resource.tainted is True

        # Property set as a Tuple
        resource = Resource()
        resource.version = self.version_tuple
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_tuple)
        assert resource.tainted is True

        # Property set as a Version
        resource = Resource()
        resource.version = fdp.version.Version(self.version_string)
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version(self.version_string)
        assert resource.tainted is True

        # Property set as a single int
        resource = Resource()

        resource.version = 15
        assert type(resource.version) is fdp.version.Version
        assert resource.version == fdp.version.Version((15, 0, 0))
        assert resource.tainted is True

        # Property set as an incompatible data type
        resource = Resource()
        with pytest.raises(TypeError):
            resource.version = [1, 2, 3]
        assert resource.tainted is False

        # Property set with setter/getter/reset
        resource = Resource()

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
