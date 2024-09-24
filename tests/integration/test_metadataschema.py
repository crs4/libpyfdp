import pytest
from rdflib import URIRef, BNode
import uuid

from fdp.metadataschema import MetadataSchema
from fdp.catalog import Catalog
from fdp.fairdatapoint import FairDataPoint
from fdp.base import LibFDPError

from test_fair_data_point import fdp_client_service, fdp_client_token, docker_compose_file
from test_fair_data_point import docker_compose_project_name, docker_cleanup


@pytest.fixture(scope="class")
def metadata_schema(fdp_client_service):
    """Returns a complete Metadata Schema instance."""

    mds = MetadataSchema(fdp_client_service)
    mds.name = "Dataset Series"
    mds.description = "Dataset Series Metadata Schema"
    mds.suggestedResourceName = "Dataset Series"
    mds.suggestedUrlPrefix = "dataset-series"
    mds.abstractSchema = False
    mds.definition = """
@prefix :         <http://fairdatapoint.org/> .
@prefix dash:     <http://datashapes.org/dash#> .
@prefix dcat:     <http://www.w3.org/ns/dcat#> .
@prefix dct:      <http://purl.org/dc/terms/> .
@prefix sh:       <http://www.w3.org/ns/shacl#> .
@prefix xsd:      <http://www.w3.org/2001/XMLSchema#> .

:DatasetShape a sh:NodeShape ;
  sh:targetClass dcat:Dataset ;
  sh:property [
    sh:path dct:issued ;
    sh:datatype xsd:dateTime ;
    sh:maxCount 1 ;
    dash:editor dash:DatePickerEditor ;
    dash:viewer dash:LiteralViewer ;
    sh:order 20 ;
  ], [
    sh:path dct:modified ;
    sh:datatype xsd:dateTime ;
    sh:maxCount 1 ;
    dash:editor dash:DatePickerEditor ;
    dash:viewer dash:LiteralViewer ;
    sh:order 21 ;
  ],  [
    sh:path dcat:theme ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    dash:editor dash:URIEditor ;
    dash:viewer dash:LabelViewer ;
    sh:order 22 ;
  ], [
    sh:path dcat:contactPoint ;
    sh:nodeKind sh:IRI ;
    sh:maxCount 1 ;
    dash:editor dash:URIEditor ;
    dash:viewer dash:LabelViewer ;
    sh:order 23 ;
  ], [
    sh:path dcat:keyword ;
    sh:nodeKind sh:Literal ;
    dash:editor dash:TextFieldEditor ;
    dash:viewer dash:LiteralViewer ;
    sh:order 24 ;
  ], [
    sh:path dcat:landingPage ;
    sh:nodeKind sh:IRI ;
    sh:maxCount 1 ;
    dash:editor dash:URIEditor ;
    dash:viewer dash:LabelViewer ;
    sh:order 25 ;
  ] .
    """

    return mds


class TestMetedataSchema:

    def test_fair_data_point_metadata_schema_create(self, fdp_client_service,
            fdp_client_token, metadata_schema):
        """Tests the creation of a Metadata Schema."""
        fair_data_point = fdp_client_service
        token = fdp_client_token
        mds = metadata_schema

        FDP = FairDataPoint(fair_data_point, token=token)

        mds.fair_data_point = FDP

        # The metadataschema has no UUID so create is the correct function to
        # call
        mds.create()

        assert mds.uuid is not None

        # Now the instance has an uuid so update function must be used instead.
        with pytest.raises(LibFDPError):
            mds.create()

    def test_fair_data_point_metadata_schema_delete(self, fdp_client_service,
            fdp_client_token, metadata_schema):
        """Tests the deletion of a Metadata Schema."""
        fair_data_point = fdp_client_service
        token = fdp_client_token
        mds = metadata_schema

        FDP = FairDataPoint(fair_data_point, token=token)

        mds.fair_data_point = FDP
        mds._uuid = None

        with pytest.raises(LibFDPError):
            mds.delete()

        # The metadataschema has no UUID so create is the correct function to
        # call
        mds.create()

        assert mds.uuid is not None

        mds.delete()
        assert mds.uuid is None

