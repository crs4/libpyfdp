import json
import os
import pytest
import requests
from requests import ConnectionError, HTTPError

from fdp.catalog import Catalog
from fdp.fairdatapoint import FairDataPoint


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir),
                        "integration",
                        "docker-compose.yml")


@pytest.fixture(scope="class")
def fdp_client_service(docker_ip, docker_services):
    """Wait for the api from Fair Data Point to become responsive"""

    port = docker_services.port_for("fdp-client", 80)

    fair_data_point = "http://%s:%s" % (docker_ip, port)

    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda:
        is_responsive(fair_data_point)
    )

    # return fair_data_point
    yield fair_data_point

    # Optionally print/log container logs for debugging.
    # for line in docker_services.get_logs('fdp').split(b'\n'):
    #     print(line)


@pytest.fixture(scope="class")
def good_catalog():
    """Returns a complete Catalog instance."""

    catalog = Catalog(iri='TheGoodCatalog')
    catalog.title = "The good Catalog"
    catalog.publisher = "The good Publisher"
    catalog.version = "1.0.0"

    return catalog


@pytest.fixture(scope="class")
def fdp_client_token(docker_ip, docker_services, fdp_client_service):
    """Requests a valid token."""

    fair_data_point = fdp_client_service

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    payload = {
        "email": "albert.einstein@example.com",
        "password": "password"
    }

    response = requests.post(fair_data_point + "/tokens",
                             data=json.dumps(payload),
                             headers=headers)

    return response.json()['token']


class TestFairDataPointConnection:
    def test_fair_data_point_no_token(self, fdp_client_service):
        """Tests the connection to the Fair Data Point with no token
           authentication.
        """
        fair_data_point = fdp_client_service

        FDP = FairDataPoint(fair_data_point)

        catalogs = FDP.find_catalogs()

        assert len(catalogs) == 0

    def test_fair_data_point_wrong_token(self, fdp_client_service):
        """Tests the connection to the Fair Data Point with  a wrong token."""
        fair_data_point = fdp_client_service

        FDP = FairDataPoint(fair_data_point, token='AWrongToken')

        with pytest.raises(HTTPError, match=r'^401 .*'):
            FDP.find_catalogs()

    def test_fair_data_point_with_token(self, fdp_client_service,
                                        fdp_client_token):
        """Tests the connection to the Fair Data Point with  a wrong token."""
        fair_data_point = fdp_client_service
        token = fdp_client_token

        FDP = FairDataPoint(fair_data_point, token=token)

        catalogs = FDP.find_catalogs()

        assert len(catalogs) == 0

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
