# SPDX-License-Identifier: Apache-2.0
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

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
import warnings

import fdp
from fdp.fairdatapointfinder import FairDataPointFinder

from rdflib import Graph, Namespace

warnings.filterwarnings("ignore")

LDP = Namespace("http://www.w3.org/ns/ldp#")


class FairDataPoint():
    """Class representing a Fair Data Point.
    """
    def __init__(self, url: str = 'http://127.0.0.1', token: str = None):
        self._url = url
        self._rest_operator = fdp.rest.RestOperator(self._url, token)
        self._finder = None

    @property
    def rest_operator(self) -> str:
        """The rest_operator."""
        return self._rest_operator

    @rest_operator.setter
    def rest_operator(self, rest_operator: fdp.rest.RestOperator) -> None:
        self._rest_operator = rest_operator

    @property
    def url(self) -> str:
        """The url of the Fair Data Point."""
        return self._url

    def find_catalogs(self) -> dict:
        """Retrieves all the catalogs belonging to the Fair Data Point.

        :return: a dictionary ```{uuid: Catalog}```
        :rtype: dict with str keys and Catalog class values
        """
        headers = {
            'Content-Type': 'text/turtle',
        }

        r = self._rest_operator.get('', headers=headers)
        _rdf = Graph().parse(data=r['content'])
        _uuids = list(_rdf.objects(None, LDP.contains, unique=True))
        _uuids = {_i.rpartition('/')[2]: _i for _i in _uuids}

        for _uuid, _iri in _uuids.items():
            _r = self.get(path=_iri, absolute=True)
            _g = Graph()
            _g.parse(data=_r['content'])

            _c = fdp.catalog.Catalog(self, _iri)
            _c._content_setter(_g)
            _uuids[_uuid] = _c

        return _uuids

    def __str__(self):
        return f'<Fair Data Point client pointing to {self._url}>'

    def get(self, path: str, uuid: str = None, **kwargs):
        """Retrieve an item from the Fair Data Point.

        :param path: the path to access
        :type path: str

        :param uuid: the uuid of the item to retrieve.
        :type path: str

        :param kwargs: custom arguments

        .. note:: passing `draft=True` as kwargs result in the retrieve of
           items in draft state instead of the published ones.

        :return: the response of the Fair Data Point server.
        :rtype: dict, see the rest module's `get` function.
        """
        if uuid:
            if kwargs.get('draft', False):
                kwargs = {k: v for k, v in kwargs.items() if k not in
                          ['draft']}

                r = self._rest_operator.get(f"{path}/{uuid}/draft", **kwargs)
            else:
                r = self._rest_operator.get(f"{path}/{uuid}", **kwargs)
        else:
            r = self._rest_operator.get(path, **kwargs)

        return r

    def create(self, path: str, payload: str, headers: dict | None, **kwargs):
        """Create a new item to the Fair Data Point.

        :param path: the path to access
        :type path: str

        :param payload: the content to update
        :type path: str

        :param headers: the headers for the update
        :type path: dict

        :param * * kwargs: custom arguments

        :return: the response of the Fair Data Point server.
        :rtype: dict, see the rest module's `post` function.
        """
        r = self._rest_operator.post(path,
                                     headers=headers,
                                     payload=payload,
                                     **kwargs)

        return r

    def update(self, path: str, uuid: str, payload: str,
               headers: dict or None, **kwargs):
        """Update an item in the Fair Data Point.

        :param path: the path to access
        :type path: str

        :param uuid: the uuid of the item to retrieve.
        :type path: str

        :param payload: the content to update
        :type path: str

        :param headers: the headers for the update
        :type path: dict

        :return: the response of the Fair Data Point server.
        :rtype: dict, see the rest module's `put` function.
        """
        if kwargs.get('draft', False):
            uri = f"{path}/{uuid}/draft"
        else:
            uri = f"{path}/{uuid}"
        r = self._rest_operator.put(uri,
                                    headers=headers,
                                    payload=payload)

        return r

    def delete(self, fairdatapointitem):
        """Deletes an instance of a Fair Data Point Item or of a derived class
        from the Fair data Point.

        :param fairdatapointitem: the item to delete

        :type fairdatapointitem: FairDataPointItem or derived class

        :raises NotPresentError: if the item is not present in the Fair Data
                                 Point
        """
        from fdp.fairdatapointitem import FairDataPointItem

        if isinstance(fairdatapointitem, FairDataPointItem):
            self._rest_operator.delete(fairdatapointitem.URL_PATH,
                                       fairdatapointitem.uuid)
        else:
            raise TypeError((f'Type {type(fairdatapointitem)} not allowed for '
                             '"delete" argument'))

    @property
    def finder(self) -> FairDataPointFinder:
        return self._finder or FairDataPointFinder(self)
