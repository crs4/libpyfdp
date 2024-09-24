import pytest
from rdflib import URIRef, BNode
import uuid

from fdp.catalog import Catalog
from fdp.fairdatapoint import FairDataPoint

from test_fair_data_point import fdp_client_service, fdp_client_token, docker_compose_file

# @pytest.fixture(scope="class")
# def good_catalog():
#     """Returns a complete Catalog instance."""
# 
#     catalog = Catalog(FairDataPoint('http://127.0.0.1:8888'), 'TheGoodCatalog')
# 
#     catalog.title = "The good Catalog"
#     catalog.publisher = "The good Publisher"
#     catalog.version = "1.0.0"
# 
#     return catalog


# @pytest.fixture(scope="class")
# def fdp_client_token(docker_ip, docker_services, fdp_client_service):
#     """Requests a valid token."""
#
#     fair_data_point = fdp_client_service
#
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
#
#     payload = {
#         "email": "albert.einstein@example.com",
#         "password": "password"
#     }
#
#     response = requests.post(fair_data_point + "/tokens",
#                              data=json.dumps(payload),
#                              headers=headers)
#
#     return response.json()['token']


class TestCatalog:
#     def test_catalog_set_iri_as_str(self):
#         """Checks if the Catalog's IRI is a URIRef."""
# 
#         catalog = Catalog(iri='A string Catalog')
#         assert type(catalog.iri) is URIRef
# 
#     def test_catalog_set_iri_as_URIRef(self):
#         """Checks if the Catalog's IRI is a URIRef."""
# 
#         catalog = Catalog(iri=URIRef('A string Catalog'))
#         assert type(catalog.iri) is URIRef
# 
#     def test_catalog_set_iri_as_BNode(self):
#         """Checks if the Catalog's IRI is a BNode."""
# 
#         catalog = Catalog(iri=BNode())
#         assert type(catalog.iri) is BNode
# 
#     def test_catalog_set_iri_as_None(self):
#         """Checks if the Catalog's IRI is a URIRef."""
# 
#         catalog = Catalog(iri=None)
#         assert type(catalog.iri) is BNode
# 
#     def test_catalog_set_iri_as_uuid(self):
#         """Checks if the Catalog's IRI is a URIRef."""
# 
#         catalog = Catalog(uuid=uuid.uuid1())
#         assert type(catalog.iri) is URIRef

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_fair_data_point_catalog_save(self, fdp_client_service,
                                          fdp_client_token, good_catalog):
        """Tests the connection to the Fair Data Point with  a wrong token."""
        fair_data_point = fdp_client_service
        token = fdp_client_token
        catalog = good_catalog

        FDP = FairDataPoint(fair_data_point, token=token)

        catalog.fair_data_point = FDP

        catalog.write()

        catalogs = FDP.find_catalogs()

        assert len(catalogs) == 1
