import pytest
# from rdflib import URIRef, BNode
# import uuid

from fdp.resourcedefinition import ResourceDefinition
from fdp.fairdatapoint import FairDataPoint
from fdp.base import LibFDPError, NotPresentError

from test_fair_data_point import fdp_client_service, fdp_client_token, docker_compose_file
from test_metadataschema import metadata_schema


# @pytest.fixture(scope="session")
# def docker_cleanup():
#     return False
#
# # @pytest.fixture(scope="session")
# # def docker_setup():
# #     return False
#
#
# @pytest.fixture(scope="session")
# def docker_compose_project_name():
#     return "libfdp_integration_tests"
#

@pytest.fixture(scope="class")
def resource_definition(fdp_client_service):
    """Returns a complete Resource Definition instance."""

    red = ResourceDefinition(fdp_client_service)
    red.name = "Dataset Series"
    red.urlPrefix = "dataset-series"
    red.add_metadataSchemaUuids("1234")

    return red


class TestResourceDefinition:

    def test_fair_data_point_resource_definition_create_and_delete(
        self, fdp_client_service, fdp_client_token, resource_definition):
        """Tests the creation of a Resource Definition."""
        fair_data_point = fdp_client_service
        token = fdp_client_token
        red = resource_definition

        FDP = FairDataPoint(fair_data_point, token=token)

        red.fair_data_point = FDP

        # The resourcedefinition has no UUID so create is the correct function
        # to call
        red.create()

        assert red.uuid is not None

        # Now the instance has an uuid so update function must be used instead.
        with pytest.raises(LibFDPError):
            red.create()

        red.get_all()

        red_2 = ResourceDefinition(FDP).get(red.uuid)

        assert red_2.uuid is not None
        assert red_2.uuid == red.uuid

        red_2.delete()
        assert red_2.uuid is None

        # Tries to delete a non existent Resource Definition
        with pytest.raises(NotPresentError):
            red.delete()
