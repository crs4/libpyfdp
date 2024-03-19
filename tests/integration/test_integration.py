import os
import pytest
import requests
from requests import ConnectionError, HTTPError

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

    return fair_data_point


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

        with pytest.raises(HTTPError):
            FDP.find_catalogs()
