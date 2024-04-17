import pytest
from rdflib import Graph, BNode, Literal

from fdp.foaf import FOAFFactory, FOAFAgent, FOAFGroup, FOAFOrganization
from fdp.foaf import FOAFPerson


@pytest.fixture(scope="session")
def good_rdf_person():
    _rdf = """
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <person#me>   a   foaf:Person ;
        foaf:name "Good Person".
    """

    return _rdf


@pytest.fixture(scope="session")
def good_rdf_organization():
    _rdf = """
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <organization#me>   a   foaf:Organization ;
        foaf:name "A Good Organization".
    """

    return _rdf


@pytest.fixture(scope="session")
def good_rdf_group():
    _rdf = """
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <group#me>   a   foaf:Group ;
        foaf:name "A Good Group".
    """

    return _rdf


@pytest.fixture(scope="session")
def good_rdf_agent():
    _rdf = """
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <agent#me>   a   foaf:Agent  ;
        foaf:name "A Good Agent".
    """

    return _rdf


class TestFOAF:
    def test_Group_set_name(self):
        foaf_obj = FOAFGroup()
        foaf_obj.name = "The Group"
        assert type(foaf_obj) is FOAFGroup
        assert type(foaf_obj.name) is str
        assert foaf_obj.name == "The Group"
        assert foaf_obj.tainted is True

    def test_Group_set_homepage(self):
        foaf_obj = FOAFGroup()
        foaf_obj.homepage = "http://www.example.com"
        assert type(foaf_obj) is FOAFGroup
        assert type(foaf_obj.homepage) is str
        assert foaf_obj.homepage == "http://www.example.com"
        assert foaf_obj.tainted is True

    def test_Group_add_members(self):
        foaf_org = FOAFGroup()
        foaf_org.name = "The Group"
        foaf_org.homepage = "http://www.example.com"

        assert type(foaf_org) is FOAFGroup
        assert type(foaf_org.name) is str
        assert foaf_org.name == "The Group"
        assert type(foaf_org.homepage) is str
        assert foaf_org.homepage == "http://www.example.com"
        assert foaf_org.tainted is True

        foaf_person_1 = FOAFPerson()
        foaf_person_1.name = "Mario Rossi"

        foaf_org.add_member(foaf_person_1)
        assert len(foaf_org.members) == 1

        # tests IRI duplication
        foaf_org.add_member(foaf_person_1)
        assert len(foaf_org.members) == 1

        foaf_person_2 = FOAFPerson()
        foaf_person_2.name = "Paolo Bianchi"
        foaf_person_2.homepage == "http://www.example_bianchi.com"
        foaf_org.add_member(foaf_person_2)
        assert len(foaf_org.members) == 2

    def test_Group_members_property(self):
        foaf_org = FOAFGroup()
        foaf_org.name = "The Group"
        foaf_org.homepage = "http://www.example.com"

        foaf_person_1 = FOAFPerson()
        foaf_person_1.name = "Mario Rossi"
        foaf_org.add_member(foaf_person_1)

        foaf_person_2 = FOAFPerson()
        foaf_person_2.name = "Paolo Bianchi"
        foaf_person_2.homepage == "http://www.example_bianchi.com"
        foaf_org.add_member(foaf_person_2)

        for foaf_member_iri, foaf_member_obj in foaf_org.members.items():
            assert foaf_member_iri in [foaf_person_1.iri, foaf_person_2.iri]
            assert type(foaf_member_obj) is FOAFPerson

    def test_Person_init(self):
        foaf_obj = FOAFPerson()
        assert type(foaf_obj) is FOAFPerson

    def test_Person_set_name_as_str(self):
        foaf_obj = FOAFPerson()
        foaf_obj.name = "Mario Rossi"
        assert type(foaf_obj) is FOAFPerson
        assert type(foaf_obj.name) is str
        assert foaf_obj.name == "Mario Rossi"
        assert foaf_obj.tainted is True

    def test_Person_set_name_as_Literal(self):
        foaf_obj = FOAFPerson()
        foaf_obj.name = Literal("Mario Rossi")
        assert type(foaf_obj) is FOAFPerson
        assert type(foaf_obj.name) is str
        assert foaf_obj.name == "Mario Rossi"
        assert foaf_obj.tainted is True

    def test_Person_set_homepage(self):
        foaf_obj = FOAFPerson()
        foaf_obj.homepage = "http://www.example.com"
        assert type(foaf_obj) is FOAFPerson
        assert type(foaf_obj.homepage) is str
        assert foaf_obj.homepage == "http://www.example.com"
        assert foaf_obj.tainted is True

    def test_Organization_set_name(self):
        foaf_obj = FOAFOrganization()
        foaf_obj.name = "The Organization"
        assert type(foaf_obj) is FOAFOrganization
        assert type(foaf_obj.name) is str
        assert foaf_obj.name == "The Organization"
        assert foaf_obj.tainted is True

    def test_Organization_set_homepage(self):
        foaf_obj = FOAFOrganization()
        foaf_obj.homepage = "http://www.example.com"
        assert type(foaf_obj) is FOAFOrganization
        assert type(foaf_obj.homepage) is str
        assert foaf_obj.homepage == "http://www.example.com"
        assert foaf_obj.tainted is True

    def test_Organization_add_members(self):
        foaf_org = FOAFOrganization()
        foaf_org.name = "The Organization"
        foaf_org.homepage = "http://www.example.com"

        assert type(foaf_org) is FOAFOrganization
        assert type(foaf_org.name) is str
        assert foaf_org.name == "The Organization"
        assert type(foaf_org.homepage) is str
        assert foaf_org.homepage == "http://www.example.com"
        assert foaf_org.tainted is True

        foaf_person_1 = FOAFPerson()
        foaf_person_1.name = "Mario Rossi"

        foaf_org.add_member(foaf_person_1)
        assert len(foaf_org.members) == 1

        # tests IRI duplication
        foaf_org.add_member(foaf_person_1)
        assert len(foaf_org.members) == 1

        foaf_person_2 = FOAFPerson()
        foaf_person_2.name = "Paolo Bianchi"
        foaf_person_2.homepage == "http://www.example_bianchi.com"
        foaf_org.add_member(foaf_person_2)
        assert len(foaf_org.members) == 2

    def test_Organization_members_property(self):
        foaf_org = FOAFOrganization()
        foaf_org.name = "The Organization"
        foaf_org.homepage = "http://www.example.com"

        foaf_person_1 = FOAFPerson()
        foaf_person_1.name = "Mario Rossi"
        foaf_org.add_member(foaf_person_1)

        foaf_person_2 = FOAFPerson()
        foaf_person_2.name = "Paolo Bianchi"
        foaf_person_2.homepage == "http://www.example_bianchi.com"
        foaf_org.add_member(foaf_person_2)

        for foaf_member_iri, foaf_member_obj in foaf_org.members.items():
            assert foaf_member_iri in [foaf_person_1.iri, foaf_person_2.iri]
            assert type(foaf_member_obj) is FOAFPerson


class TestFOAFGetAgent:
    def test_get_agent_Person(self, good_rdf_person):
        _graph = Graph().parse(data=good_rdf_person)

        agent = FOAFFactory().get_agent(_graph)

        assert type(agent) is FOAFPerson

    def test_get_agent_Organization(self, good_rdf_organization):
        _graph = Graph().parse(data=good_rdf_organization)

        agent = FOAFFactory().get_agent(_graph)

        assert type(agent) is FOAFOrganization

    def test_get_agent_Group(self, good_rdf_group):
        _graph = Graph().parse(data=good_rdf_group)

        agent = FOAFFactory().get_agent(_graph)

        assert type(agent) is FOAFGroup

    def test_get_agent_Agent(self, good_rdf_agent):
        _graph = Graph().parse(data=good_rdf_agent)

        agent = FOAFFactory().get_agent(_graph)

        assert type(agent) is FOAFAgent

    # def test_get_agent_incompatible_classes(self, good_rdf_group,
    #                                         good_rdf_person,
    #                                         good_rdf_organization):
    #     _graph = Graph().parse(data=good_rdf_group)
    #     _graph += Graph().parse(data=good_rdf_person)
    #     _graph += Graph().parse(data=good_rdf_organization)

    #     agent = FOAFFactory().get_agent(_graph)

    #     assert type(agent) is FOAFAgent
