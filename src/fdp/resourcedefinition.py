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
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
from __future__ import annotations

import json

from fdp.fairdatapoint import FairDataPoint
from fdp.fairdatapointitem import FairDataPointItem
from fdp.base import SetEncoder
from fdp.metadataschema import MetadataSchema


class ResourceDefinition(FairDataPointItem):
    """Class representing a Fair Data Point Resource Definition.
    """

    URL_PATH = 'resource-definitions'
    CONTENT_TYPE = 'application/json'

    _READ_PROPERTIES = ['uuid', 'targetClassUris']
    _WRITE_PROPERTIES = ['name', 'urlPrefix', 'metadataSchemaUuids',
                         'children', 'externalLinks']
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    def __init__(self, fair_data_point: FairDataPoint = None,
                 uuid: str = None):
        super().__init__(fair_data_point)

        self._uuid = uuid

    def __str__(self):
        return (f"<ResourceDefinition uuid={self._uuid}, name=\"{self._name}\""
                ", {}>".format("tainted" if self._tainted else "not tainted"))

    @property
    def name(self) -> str:
        """The ``name`` property."""
        return self._name

    @name.setter
    def name(self, name: str):
        if type(name) is str:
            self._name = name
        else:
            raise TypeError

        self._tainted = True

    @property
    def urlPrefix(self) -> str:
        """Get or set the ``urlPrefix`` property of the Resource Definition.
        """
        return self._urlPrefix

    @urlPrefix.setter
    def urlPrefix(self, urlPrefix: str):

        if type(urlPrefix) is str:
            self._urlPrefix = urlPrefix
        else:
            raise TypeError

        self._tainted = True

    @property
    def metadataSchemaUuids(self) -> list:
        """Get the Metadata Schemas's UUID of the Resource Definition.

        .. note:: the setter for this property is the
            ``add_metadataSchemaUuids`` function.
        """
        if self._metadataSchemaUuids:
            return list(self._metadataSchemaUuids)

        return []

    def add_metadataSchemaUuids(self, metadata_schema: str | MetadataSchema |
                                list[str] | list[MetadataSchema]):
        """Adds a Metadata Schema to the Resource Definition.

        :param metadata_schema: the UUID of the Metadata Schema or the
            MetadataSchema instance to add to the Resource Definition
        :type metadata_schema: str or MetadataSchema instance or a list of str
            or MetadataSchema instances

        :returns: none

        :raises TypeError: if the ``metadata_schema`` is not a str nor a
            MetadataSchema instance or a list of them
        """
        if type(metadata_schema) is not list:
            metadata_schema = [metadata_schema]

        for _schema in metadata_schema:
            if type(_schema) is str:
                _new_metadata_schema = _schema
            elif type(_schema) is MetadataSchema:
                if _schema.uuid is None:
                    raise ValueError(('The Metadata Schema UUID is None. '
                                      'Metadata Schema must have a Fair Data '
                                      'Point provided UUID.'))

                _new_metadata_schema = _schema.uuid
            else:
                raise TypeError((f'Type {type(metadata_schema)} not allowed '
                                 'for "metadata_schema" argument.'))

            # pylint: disable=access-member-before-definition
            if self._metadataSchemaUuids is None:
                # pylint: disable=attribute-defined-outside-init
                self._metadataSchemaUuids = {_new_metadata_schema}
            else:
                self._metadataSchemaUuids.add(_new_metadata_schema)

    @property
    def children(self) -> dict:
        """Get the children of the Resource Definition.

        .. note:: the setter for this property is the ``add_children``
            function.
        """
        # pylint: disable=no-member
        return self._children or []

    # XXX: Check on attributes and add listView (change the warning
    # accordingly)
    def add_children(self, children: dict | list[dict]):
        """Adds one or more children to the the Resource Definition.

        :param children: the children to add to the Resource Definition.
                         The dictionary must be of the type:

        .. code-block:: python

            {
                "resourceDefinitionUuid": string,
                "relationUri": string
            }

        :type children: dict or list[dict]

        :returns: none

        :raises TypeError: if the ``children`` is not a dict nor a
            list of dict or is missing of one mandatory attribute.

        .. note::
            the function does not check for duplication.

        .. warning::
            the ``child`` dictionary is incomplete. It lacks the listView
            attribute.
        """
        if type(children) is not list:
            children = [children]

        for _child in children:

            if _child['resourceDefinitionUuid'] is None:
                raise TypeError("resourceDefinitionUuid must not be None")

            _new_child = dict([
                ('resourceDefinitionUuid', _child['resourceDefinitionUuid']),
                ('relationUri', _child['relationUri']),
                ('listView', _child['listView']),
            ])

        #     _new_child = {child.uuid: _new_child}
        # else:
        #     raise TypeError((f'Type {type(child)} not allowed for '
        #                      '"child" argument'))

            # pylint: disable=access-member-before-definition
            if self._children is None:
                # pylint: disable=attribute-defined-outside-init
                self._children = [_new_child]
            else:
                self._children.append(_new_child)

    @property
    def externalLinks(self) -> list[dict]:
        """Get the externalLinks property of the Resource Definition.

        .. note:: the setter for this property is the ``add_externalLinks``
            function.
        """
        # pylint: disable=no-member
        return self._externalLinks or []

    # XXX: Check on attributes
    def add_externalLinks(self, links: dict | list[dict]):
        """Adds external links to the the Resource Definition.

        :param links: the external link or a list of external links to add to
                      the Resource Definition. The dictionary must be of the
                      type:

        .. code-block:: python

            {
                "title": string,
                "propertyUri": string
            }

        :type links: dict or list[dict]

        :returns: none

        :raises TypeError: if the ``links`` is not a dict nor a
            list of dict
        """
        if type(links) is not list:
            links = [links]

        for _link in links:
            _new_link = {
                "title": _link['title'],
                "propertyUri": _link['propertyUri']
            }

            if self._externalLinks is None:
                self._externalLinks = [_new_link]
            else:
                self._externalLinks.append(_new_link)

    def _content(self):
        content_dict = {k: getattr(self, k) for k in
                        self._WRITE_PROPERTIES}

        return json.dumps(content_dict, cls=SetEncoder)

    def _content_setter(self, content: dict):
        for k in content:
            v = content[k]

            if k in self._WRITE_PROPERTIES:
                if isinstance(v, (list, dict)):
                    func = getattr(self, f"add_{k}")
                    func(v)
                else:
                    setattr(self, k, v)
            elif k in self._READ_PROPERTIES:
                setattr(self, f"_{k}", v)
            else:
                print(f"Unknown {k}: {v}")

    def get_by_name(self,
                    name: str,
                    ignore_case: bool = False):
        """Retrieve the Resource Definition with the given name.

        :param name: the name of the resource definition to retrieve
        :type path: str

        :param ignore_case: if True, performs a case-insensitive search
        :type path: bool

        :return: the Resource Definition or None
        :rtype: ResourceDefinition
        """
        rdefs = self.list()
        for rdef in rdefs:
            if ignore_case:
                if rdef.name.lower() == name.lower():
                    return rdef
            else:
                if rdef.name == name:
                    return rdef

    def get_by_uuid(self,
                    uuid: str):
        """Retrieve the Resource Definition with the given uuid.

        :param uuid: the uuid of the resource definition to retrieve
        :type path: str

        :return: the Resource Definition or None
        :rtype: ResourceDefinition
        """
        rd = self._fair_data_point.get(
            self.URL_PATH,
            uuid=uuid)['content']

        _item = self.__class__(self._fair_data_point)
        _item._content_setter(rd)

        return _item

    def list(self):
        """Retrieve the list of all the Metadata Schemas.

        :return: a list of the Metadata Schema
        :rtype: list[MetadataSchema]
        """
        rd_list = self._fair_data_point.get(
            self.URL_PATH)['content']

        return_list = []

        for rd in rd_list:
            _item = self.__class__(self._fair_data_point)
            _item._content_setter(rd)
            return_list.append(_item)

        return return_list
