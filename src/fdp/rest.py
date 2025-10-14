# Copyright 2024-2025 CRS4 - Center for Advanced Studies, Research and
# Development in Sardinia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
            raise_for_status: bool = True,
            absolute: bool = False, **parameters) -> dict:
        """Executes a GET query to the Fair Data Point.

        :param uri: the relative path of the resource
        :type uri: str

        :param headers: specific headers to add or override to the default
                        one
        :type headers: dict


        :param raise_for_status: raise an HTTPError if the query returns an
                               error code (>=400). Overrides the instance
                               default.
        :type raise_for_status: bool

        :param absolute: the uri is considered absolute (does not prepend the
                         Fair Data Point URL)
        :type absolute: bool

        :param parameters: dict parameters for the query, if any
        :type parameters: dict

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

        # print(
        #     "GET",
        #     uri if absolute else f"{self.base_url}/{uri}",
        #     actual_headers,
        #     parameters
        # )
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

    def delete(self, uri: str = None, uuid: str = None,
               raise_for_status: bool = None) -> dict:
        """Executes a DELETE query to the Fair Data Point.

        :param uri: the relative path of the resource
        :type uri: str

        :param uuid: the UUID of the instance to delete

        :param raise_for_status: raise an HTTPError if the query returns an
                               error code (>=400). Overrides the instance
                               default.
        :type raise_for_status: bool

        :return: a dictionary ``{'code': int}``
        :rtype: dict
        """

        default_headers = {
            'Authorization': f'Bearer {self.token}'
        }

        actual_headers = default_headers

        response = requests.request(
            "DELETE",
            f"{self.base_url}/{uri}/{uuid}",
            headers=actual_headers,
        )

        self.raise_http_error(response, raise_for_status)

        return {
            'code': response.status_code
               }

    def __str__(self):
        return (f'<Fair Data Point Rest Operator pointing to '
                f'{self.base_url}, token="{self.token}">')
