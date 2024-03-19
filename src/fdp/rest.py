# docstring references:
# https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
# https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
# https://www.sphinx-doc.org/en/master/usage/domains/python.html

import json
import requests


class RestOperator(object):
    """Class that implements REST operations on the Fair Data Point."""
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url
        self.token = token
        self.response = None
        self.raise_for_status = True

    def raise_http_error(self, response: requests.Response,
                         raise_for_status: bool = None):
        if raise_for_status is not None:
            if raise_for_status is True:
                response.raise_for_status()
        elif self.raise_for_status:
            response.raise_for_status()

    def put(self, uri: str = None, headers: dict = None,
            payload: dict = None, raise_for_status: bool = None) -> dict:
        """Executes a PUT query to the Fair Data Point.

        :param uri: the relative path of the resource
        :type uri: str

        :param headers: specific headers to add or override to the default
                        one
        :type headers: dict

        :param payload: payload for the query, if any
        :type payload: dict

        :param raise_for_status: raise an HTTPError if the query returns an
                               error code (>=400). Overrides the instance
                               default.
        :type raise_for_status: bool

        :return: a dictionary ``{'code': int, 'content': dict or text}``
        :rtype: dict
        """

        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        actual_headers = ({
            **default_headers, **headers} if headers is not None else
            default_headers)

        payload = json.dumps(payload)

        response = requests.request(
            "PUT",
            f"{self.base_url}/{uri}",
            headers=actual_headers,
            data=payload
        )

        self.raise_http_error(response, raise_for_status)

        return {
            'code': response.status_code,
            'content': (
                response.json()
                if response.headers.get('content-type') == 'application/json'
                else response.text)
               }

    def post(self, uri: str = None, headers: dict = None,
             payload: dict = None, raise_for_status: bool = True) -> dict:
        """Executes a POST query to the Fair Data Point.

        :param uri: the relative path of the resource
        :type uri: str

        :param headers: specific headers to add or override to the default
                        one
        :type headers: dict

        :param payload: payload for the query, if any
        :type payload: dict

        :param raise_for_status: raise an HTTPError if the query returns an
                               error code (>=400). Overrides the instance
                               default.
        :type raise_for_status: bool

        :return: a dictionary ``{'code': int, 'content': dict or text}``
        :rtype: dict
        """
        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        actual_headers = ({
            **default_headers, **headers} if headers is not None else
            default_headers)

        # payload = json.dumps(payload)

        response = requests.request(
            "POST",
            f"{self.base_url}/{uri}",
            headers=actual_headers,
            data=payload
        )

        self.raise_http_error(response, raise_for_status)

        return {
            'code': response.status_code,
            'content': (
                response.json()
                if response.headers.get('content-type') == 'application/json'
                else response.text)
               }

    def get(self, uri: str = None, headers: dict = None,
            parameters: dict = None, raise_for_status: bool = True,
            absolute: bool = False) -> dict:
        """Executes a GET query to the Fair Data Point.

        :param uri: the relative path of the resource
        :type uri: str

        :param headers: specific headers to add or override to the default
                        one
        :type headers: dict

        :param parameters: dict parameters for the query, if any
        :type parameters: dict

        :param raise_for_status: raise an HTTPError if the query returns an
                               error code (>=400). Overrides the instance
                               default.
        :type raise_for_status: bool

        :param absolute: the uri is considered absolute (does not prepend the
                         Fair Data Point URL)
        :type absolute: bool

        :return: a dictionary ``{'code': int, 'content': dict or text}``
        :rtype: dict
        """

        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
            if self.token is not None else None,
        }

        actual_headers = ({
                **default_headers, **headers
            } if headers is not None else default_headers)

        response = requests.request(
            "GET",
            uri if absolute else f"{self.base_url}/{uri}",
            headers=actual_headers,
            params=parameters
        )

        self.raise_http_error(response, raise_for_status)

        return {
            'code': response.status_code,
            'content': (
                response.json()
                if response.headers.get('content-type') == 'application/json'
                else response.text)
               }
