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

import json
import requests

from rdflib import Graph
from rdflib.namespace import DCAT, RDF

from fdp.base import LibFDPError, NotPresentError
from fdp.fairdatapoint import FairDataPoint
from fdp.version import Version


class FairDataPointItem():
    """Base class for all the Fair Data Point entities."""

    _READ_PROPERTIES = []
    _WRITE_PROPERTIES = []
    _CLASS_PROPERTIES = []
    _CLASS_PROPERTIES_MAPPING = {}
    _CLASS_PROPERTIES_MAPPING_INVERTED = {}

    __frozen = False

    def __init__(self,
                 fair_data_point: FairDataPoint = None):

        self._CLASS_PROPERTIES_MAPPING_INVERTED = {
            v: k for k, v in self._CLASS_PROPERTIES_MAPPING.items()}

        for _p in self._CLASS_PROPERTIES:
            setattr(self.__class__, f'_{_p}', None)

        self._fair_data_point = (
            fair_data_point or
            FairDataPoint('http://127.0.0.1'))

        self._rdf = None
        self._iri = None
        self._uuid = None
        self._tainted = False

        self.__frozen = True

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def properties(self):
        """The class properties.

        :returns: a list of class properties.
        :rtype: list of str
        """
        return self._WRITE_PROPERTIES

    def publish(self, version, description: str = None):
        if description is None:
            description = self.description

        if len(description) == 0:
            raise ValueError("Description must be a non empty string.")

        version = Version(version)

        return self._publish(version, description)

    def _publish(self, version, description: str):

        headers = {
            'Content-Type': self.CONTENT_TYPE
        }

        payload = json.dumps({
            "major": version.major,
            "minor": version.minor,
            "patch": version.patch,
            "version": version.as_str(),
            "description": description,
            "published": False
        })

        self._fair_data_point.create(
            f"{self.URL_PATH}/{self.uuid}/versions",
            payload=payload,
            headers=headers)

    def _write(self, allow_update: bool = True,
               allow_duplicates: bool = False):
        """Writes the instance attributes to the Fair Data Point.
        :param allow_update: if true, override the instance's attribute;
        :type allow_update: bool

        :param allow_duplicates: write the catalog even if there are
                                  other catalogs with the same name.
        :type allow_duplicates: bool

        :raises AlreadyPresentError: if the catalog already exists in the Fair
                                     Data Point and allow_duplicates is not
                                     set.
        """

        headers = {
            'Content-Type': self.CONTENT_TYPE
        }

        payload = self._content()

        response = self._fair_data_point.create(self.URL_PATH,
                                                payload=payload,
                                                headers=headers)

        if self.CONTENT_TYPE == 'application/json':
            self._uuid = response['content']['uuid']
        elif self.CONTENT_TYPE == 'text/turtle':
            _rdf = Graph().parse(data=response['content'])
            self._uuid = _rdf.value(
                predicate=RDF.type,
                object=DCAT.Resource)
#             self._uuid = Path(urlparse(self._uuid).path).name

        return response['content']

    def _update(self, **kwargs):
        """Updates the instance attributes to the Fair Data Point.
        """

        headers = {
            'Content-Type': self.CONTENT_TYPE
        }

        payload = self._content()

        try:
            element = self._fair_data_point.update(self.URL_PATH,
                                                   uuid=self.uuid,
                                                   payload=payload,
                                                   headers=headers,
                                                   **kwargs)

            self._content_setter(element['content'])
        except requests.exceptions.HTTPError as htex:
            if htex.response.status_code == 404:
                raise NotPresentError()
            else:
                raise htex

    def _get(self, uuid: str, **kwargs):
        if uuid is not None:
            try:
                if kwargs.get('absolute', False):
                    element = self._fair_data_point.get(
                        '', uuid=uuid, **kwargs)['content']
                else:
                    element = self._fair_data_point.get(
                        self.URL_PATH, uuid=uuid, **kwargs)['content']

                new_item = self.__class__(self._fair_data_point)
                new_item._content_setter(element)
            except requests.exceptions.HTTPError as htex:
                if htex.response.status_code == 404:
                    raise NotPresentError()
                else:
                    raise htex

            return new_item
        else:
            return None

    def _get_all(self, **kwargs):
        element_list = self._fair_data_point.get(
            self.URL_PATH, **kwargs)['content']
        item_list = []

        for element in element_list:
            new_item = self.__class__(self._fair_data_point)
            new_item._content_setter(element)
            item_list.append(new_item)

        return item_list

    def _delete(self):
        """Deletes the instance from the Fair Data Point."""
        try:
            self._fair_data_point.delete(self)
        except requests.exceptions.HTTPError as htex:
            if htex.response.status_code == 404:
                raise NotPresentError()
            else:
                raise htex

    @property
    def draft(self) -> str:
        """The ``draft`` attribute.

        .. note::
            This attribute has no setter.
        """
        return self._draft

    @property
    def latest(self) -> str:
        """The ``latest`` attribute.

        .. note::
            This attribute has no setter.
        """
        return self._latest

    @property
    def uuid(self) -> str:
        """The ``uuid`` attribute.

        .. note::
            This attribute has no setter.
        """
        return self._uuid

    @property
    def fair_data_point(self):
        """The ``dcterms:isPartOf`` (Catalog's Fair Data Point) property."""
        return self._fair_data_point

    @fair_data_point.setter
    def fair_data_point(self, fair_data_point: str or
                        FairDataPoint):
        if isinstance(fair_data_point, str):
            self._fair_data_point = FairDataPoint(
                fair_data_point)
        elif isinstance(fair_data_point, FairDataPoint):
            self._fair_data_point = fair_data_point

    def create(self):
        """Creates a new Fair Data Point Item."""
        if self._uuid:
            raise LibFDPError(
                "The instance has an UUID: use update() function instead.")
        else:
            self._write()

    def update(self, **kwargs):
        """Update an existing Fair Data Point Item."""
        if not self._uuid:
            raise LibFDPError(
                "The instance has no UUID: use create() function instead.")
        else:
            self._update(**kwargs)

    def delete(self):
        """Deletes a Fair Data Point Item from the Fair Data Point. On success, UUID
        attribute is set to None"""
        if self._uuid is None:
            raise LibFDPError(
                "The instance has no UUID.")
        else:
            self._delete()
            self._uuid = None

    def get(self, uuid, **kwargs):
        """Retrieves all the Fair Data Point Item of the derived class from the
        Fair Data Point.

        :param uuid: the UUID of the Item to retrieve
        :type uuid: str

        :returns: the Fair Data Point item

        :raises TypeError: if the ``uuid`` is None
        :raises NotPresentError: if the ``uuid`` is not present in the Fair
            Data Point

        """
        return self._get(uuid, **kwargs)

    def get_all(self, **kwargs):
        """Retrieves all the Fair Data Point Item of the derived class from the
        Fair Data Point."""
        return self._get_all(**kwargs)

    def inspect(self, internals: bool = False):
        """Retrieves the value of the class properties.

        :return: a dictionary with the class's properties.
        :rtype: dict
        """
        _inspect = {_p: getattr(self, f"_{_p}") for _p in
                    self._CLASS_PROPERTIES}

        if internals:
            _inspect.update({
                "iri": self._iri,
                "uuid": self._uuid,
                "tainted": self._tainted,
            })

        return _inspect

    def check_duplicates(self, ignore_case: bool = False):
        """Commodity function that checks if the given Item is already present
        in the Fair Data Point.

        The check is performed against the name of the item.

        :param ignore_case: wether or not match case
        :type ignore_case: bool

        :returns: True if an item with the same name is already present in
            the Fair Data Point, False otherwise
        :rtype: bool
        """
        element_list = self.get_all()
        for element in element_list:
            if ignore_case:
                if element.name.lower() == self.name.lower():
                    return True
            else:
                if element.name == self.name:
                    return True

        return False
