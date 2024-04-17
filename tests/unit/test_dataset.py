import pytest
# from rdflib import URIRef, BNode

from fdp.dataset import Dataset
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
def good_dataset():
    """Returns a complete Dataset instance."""

    dataset = Dataset(FairDataPoint('http://127.0.0.1:8888'), 'TheGoodDataset')

    dataset.title = "The good Dataset"
    dataset.publisher = "The good Publisher"
    dataset.version = "1.0.0"

    return dataset


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


# class TestDataset:
#     def test_dataset_set_title_as_None(self):
#         """Checks if the Dataset's IRI is None."""
#
#         dataset = Dataset()
#         assert dataset.title is None
#
#     def test_dataset_set_title_as_str(self):
#         """Checks if the Dataset's IRI is a Literal."""
#
#         dataset = Dataset()
#         dataset.title = 'A string title'
#         assert type(dataset.title) is Literal
#
#     def test_dataset_set_title_as_Literal(self):
#         """Checks if the Dataset's IRI is a Literal."""
#
#         dataset = Dataset()
#         dataset.title = Literal('A string title')
#         assert type(dataset.title) is Literal
