# import json
# import os
import pytest
from rdflib import URIRef, BNode
# import requests
# from requests import ConnectionError, HTTPError
import uuid

from fdp.catalog import Catalog
from fdp.fairdatapoint import FairDataPoint


# def is_responsive(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return True
#     except ConnectionError:
#         return False
#
#
# @pytest.fixture(scope="session")
# def docker_compose_file(pytestconfig):
#     return os.path.join(str(pytestconfig.rootdir),
#                         "integration",
#                         "docker-compose.yml")
#
#
# @pytest.fixture(scope="class")
# def fdp_client_service(docker_ip, docker_services):
#     """Wait for the api from Fair Data Point to become responsive"""
#
#     port = docker_services.port_for("fdp-client", 80)
#
#     fair_data_point = "http://%s:%s" % (docker_ip, port)
#
#     docker_services.wait_until_responsive(
#         timeout=30.0, pause=0.1, check=lambda:
#         is_responsive(fair_data_point)
#     )
#
#     # return fair_data_point
#     yield fair_data_point
#
#     # Optionally print/log container logs for debugging.
#     # for line in docker_services.get_logs('fdp').split(b'\n'):
#     #     print(line)


@pytest.fixture(scope="class")
def good_catalog():
    """Returns a complete Catalog instance."""

    catalog = Catalog(FairDataPoint('http://127.0.0.1:8888'), 'TheGoodCatalog')

    catalog.title = "The good Catalog"
    catalog.publisher = "The good Publisher"
    catalog.version = "1.0.0"

    return catalog


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
    def test_catalog_set_iri_as_str(self):
        """Checks if the Catalog's IRI is a URIRef."""

        catalog = Catalog(iri='A string Catalog')
        assert type(catalog.iri) is URIRef

    def test_catalog_set_iri_as_URIRef(self):
        """Checks if the Catalog's IRI is a URIRef."""

        catalog = Catalog(iri=URIRef('A string Catalog'))
        assert type(catalog.iri) is URIRef

    def test_catalog_set_iri_as_BNode(self):
        """Checks if the Catalog's IRI is a BNode."""

        catalog = Catalog(iri=BNode())
        assert type(catalog.iri) is BNode

    def test_catalog_set_iri_as_None(self):
        """Checks if the Catalog's IRI is a URIRef."""

        catalog = Catalog(iri=None)
        assert type(catalog.iri) is BNode

    def test_catalog_set_iri_as_uuid(self):
        """Checks if the Catalog's IRI is a URIRef."""

        catalog = Catalog(uuid=uuid.uuid1())
        assert type(catalog.iri) is URIRef
