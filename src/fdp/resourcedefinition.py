# pylint: disable=missing-module-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
from __future__ import annotations

import fdp.fairdatapoint
from fdp.base import FairDataPointItem
from fdp.metadataschema import MetadataSchema


class ResourceDefinition(FairDataPointItem):
    """Class representing a Fair Data Point Resource Definition.
    """

    URL_PATH = 'resource-definitions'
    CONTENT_TYPE = 'application/json'

    _CLASS_PROPERTIES = ['name', 'url_prefix', 'metadata_schemas',
                         'children', 'external_links']

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 uuid: str = None):
        super().__init__(fair_data_point)

        self._uuid = uuid

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
    def url_prefix(self) -> str:
        """Get or set the ``URL Prefix`` property of the Resource Definition.

        :raises TypeError: if the ``url_prefix`` is not a str
        """
        return self._url_prefix

    @url_prefix.setter
    def url_prefix(self, url_prefix: str):

        if type(url_prefix) is str:
            self._url_prefix = url_prefix
        else:
            raise TypeError

        self._tainted = True

    @property
    def metadata_schemas(self) -> set:
        """Get the Metadata Schemas's UUID of the Resource Definition.

        .. note:: the setter for this property is the ``add_metadata_schema``
            function.
        """
        return self._metadata_schemas or set()

    def add_metadata_schema(self, metadata_schema: str or MetadataSchema):
        """Adds a Metadata Schema to the Resource Definition.

        :param metadata_schema: the UUID of the Metadata Schema or the
            MetadataSchema instance to add to the Resource Definition
        :type metadata_schema: str or MetadataSchema instance

        :returns: none

        :raises TypeError: if the ``metadata_schema`` is not a str nor a
            MetadataSchema instance
        """
        if type(metadata_schema) is str:
            _new_metadata_schema = metadata_schema
        elif type(metadata_schema) is MetadataSchema:
            if metadata_schema.uuid is None:
                raise ValueError(('The Metadata Schema UUID is None. '
                                  'Metadata Schema must have a Fair Data '
                                  'Point provided UUID.'))

            _new_metadata_schema = metadata_schema.uuid
        else:
            raise TypeError((f'Type {type(metadata_schema)} not allowed for '
                             '"metadata_schema" argument.'))
        # pylint: disable=access-member-before-definition
        if self._metadata_schemas is None:
            # pylint: disable=attribute-defined-outside-init
            self._metadata_schemas = {_new_metadata_schema}
        else:
            self._metadata_schemas.add(_new_metadata_schema)

    @property
    def children(self) -> dict:
        """Get the children of the Resource Definition.

        .. note:: the setter for this property is the ``add_child``
            function.
        """
        # pylint: disable=no-member
        return self._children or {}

    def add_child(self, child: str or ResourceDefinition,
                  relation_uri: str,
                  list_view_title: str or None = None,
                  list_view_tags_uri: str or None = None):
        """Adds a child to the the Resource Definition."""

        _new_child = dict([
            ('relationUri', relation_uri),
            ('listView_title', list_view_title),
            ('listView_tagsUri', list_view_tags_uri)
        ])

        if type(child) is str:
            _new_child = {child: _new_child}
        elif type(child) is ResourceDefinition:
            if child.uuid is None:
                raise ValueError(('The Resource Definition UUID is None. '
                                  'Resource Definition must have a Fair '
                                  'Data Point provided UUID.'))

            _new_child = {child.uuid: _new_child}
        else:
            raise TypeError((f'Type {type(child)} not allowed for '
                             '"child" argument'))

        # pylint: disable=access-member-before-definition
        if self._children is None:
            # pylint: disable=attribute-defined-outside-init
            self._children = _new_child
        else:
            self._children.update(_new_child)
