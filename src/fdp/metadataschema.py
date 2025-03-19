# pylint: disable=missing-module-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
# pylint: disable=invalid-name
from __future__ import annotations
import json
import rdflib

from fdp.fairdatapoint import FairDataPoint
from fdp.base import FairDataPointItem
from fdp.base import SetEncoder
from fdp.base import NotPresentError
from fdp.version import Version


class MetadataSchema(FairDataPointItem):
    """Class representing a Fair Data Point Metadata Schema."""

    URL_PATH = 'metadata-schemas'
    CONTENT_TYPE = 'application/json'

    _READ_PROPERTIES = ['extendSchemaUuids', 'childSchemaUuids', 'latest',
                        'uuid', 'draft', 'versions', 'lastVersion', 'version',
                        'published']
    _WRITE_PROPERTIES = ['name', 'suggestedResourceName', 'description',
                         'abstractSchema', 'extendsSchemaUuids',
                         'suggestedUrlPrefix',
                         'definition']
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    def __init__(self, fair_data_point: FairDataPoint = None,
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
    def description(self) -> str:
        """The ``description`` attribute."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        if type(description) is str:
            self._description = description
        else:
            raise TypeError

        self._tainted = True

    @property
    def definition(self) -> str:
        """Get or set the ``definition`` property of the Metadata Schema.

        .. warning:: the definitiona MUST be a RDF string

        :raises TypeError: if the ``definition`` is not a str
        :raises ValueError: if the string does not contain a valid RDF graph
        """
        return self._definition

    @definition.setter
    def definition(self, definition: str) -> None:
        if type(definition) is str:
            try:
                rdflib.Graph().parse(data=definition)
            except rdflib.exceptions.ParserError as tex:
                raise ValueError(
                    "The definition must be an RDF string.") from tex
        else:
            raise TypeError

        self._definition = definition

        self._tainted = True

    @property
    def suggestedResourceName(self) -> str:
        """The ``suggestedResourceName`` property."""
        return self._suggestedResourceName

    @suggestedResourceName.setter
    def suggestedResourceName(self, suggestedResourceName: str | None):
        if type(suggestedResourceName) is str:
            self._suggestedResourceName = suggestedResourceName
        elif suggestedResourceName is None:
            self._suggestedResourceName = None
        else:
            raise TypeError(f"Value '{suggestedResourceName}' for "
                            "suggestedResourceName property is not valid.")

        self._tainted = True

    @property
    def suggestedUrlPrefix(self) -> str:
        """The ``suggestedUrlPrefix`` property."""
        return self._suggestedUrlPrefix

    @suggestedUrlPrefix.setter
    def suggestedUrlPrefix(self, suggestedUrlPrefix: str):
        if type(suggestedUrlPrefix) is str:
            self._suggestedUrlPrefix = suggestedUrlPrefix
        elif suggestedUrlPrefix is None:
            self._suggestedUrlPrefix = None
        else:
            raise TypeError(f"Value '{suggestedUrlPrefix}' for "
                            "suggestedUrlPrefix property is not valid.")

        self._tainted = True

    @property
    def abstractSchema(self) -> str:
        """The ``abstractSchema`` property."""
        return self._abstractSchema

    @abstractSchema.setter
    def abstractSchema(self, abstractSchema: str):
        if type(abstractSchema) is bool:
            self._abstractSchema = abstractSchema
        else:
            raise TypeError

        self._tainted = True

    @property
    def extendsSchemaUuids(self) -> set:
        """Get the list of the Schemas' UUIDs extended by the Metadata Schema.

        .. note:: the setter for this property is the ``add_extendSchemaUuids``
            function.
        """
        return self._extendsSchemaUuids or set()

    def add_extendsSchemaUuids(self, metadata_schema: str | MetadataSchema |
                               list[str] | list[MetadataSchema]):
        """Adds Metadata Schemas (one or a list) to the list of Metadata Schema
        extended.

        :param metadata_schema: the UUID of the Metadata Schema or the
            MetadataSchema instance to add ora a list of them
        :type metadata_schema: str or MetadataSchema instance or a list of str
            or MetadataSchema instances

        :returns: none

        :raises TypeError: if the ``metadata_schema`` is not a str nor a
            MetadataSchema instance or a list of them
        """
        if type(metadata_schema) is not list:
            metadata_schema = [metadata_schema]

        for _schema in metadata_schema:
            if _schema is not None:
                if type(_schema) is str:
                    _new_metadata_schema = _schema
                elif type(_schema) is MetadataSchema:
                    if _schema.uuid is None:
                        raise ValueError(
                            ('The Metadata Schema UUID is None. Metadata '
                             'Schema must have a Fair Data ' 'Point provided '
                             'UUID.'))

                    _new_metadata_schema = _schema.uuid
                else:
                    raise TypeError(
                        (f'Type {type(_schema)} not allowed for '
                         '"metadata_schema" argument.'))

                # pylint: disable=access-member-before-definition
                if self._extendsSchemaUuids is None:
                    # pylint: disable=attribute-defined-outside-init
                    self._extendsSchemaUuids = {_new_metadata_schema}
                else:
                    self._extendsSchemaUuids.add(_new_metadata_schema)

#     @property
#     def version(self) -> str:
#         """The version attribute."""
#         return self._version
#
#     @version.setter
#     def version(self, version: str or Version) -> str:
#         """The version attribute."""
#         if isinstance(version, str):
#             self._version = Version(version)
#         elif isinstance(version, Version):
#             self._version = version
#         else:
#             raise ValueError

    def publish(self, version: Version = None, comment: str = None):
        if self._uuid is None:
            raise NotPresentError((
                "Attempting to publish a Metadata Schema that does not exist. "
                "Metadata Schema must be present in the Fair Data Point to be "
                "published."))

        payload = {
            "version": self._version.as_str(),
            "description": comment,
            "published": "true"
        }

        _ = self._fair_data_point._rest_operator.post(
            f'metadata-schemas/{self._uuid}/versions',
            payload=payload)

#     def __str__(self):
#         return (f"<MetadataSchema uuid={self._uuid}, name=\"{self._name}\", "
#                 f"version={self._version}, "
#                 "{}>".format("Tainted" if self._tainted else "NotTainted"))

    def __str__(self):
        return (f"<MetadataSchema uuid={self._uuid}, name=\"{self._name}\", "
                "{}{}>".format("tainted" if self._tainted else "not tainted",
                               ", draft" if self._draft else ""))

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

    def create(self):
        """Creates a new Metadata Schema."""
        super().create()

    def delete(self):
        """Deletes a Metadata Schema from the Fair Data Point. On success, UUID
        attribute is set to None"""
        super().delete()

    def update(self):
        """Deletes a Metadata Schema from the Fair Data Point. On success, UUID
        attribute is set to None"""
        super().update(draft=True)

    def get_by_name(self,
                    name: str,
                    ignore_case: bool = False,
                    draft: bool = False):
        """Retrieve the Metadata Schema with the given name.

        :param name: the name of the metadata schema to retrieve
        :type path: str

        :param ignore_case: if True, performs a case-insensitive search
        :type path: bool

        :param draft: if True, retrieves the draft of the Metadata Schema
        drafts, if any
        :type path: bool

        :return: the Metadata Schema or None
        :rtype: MetadataSchema
        """
        mss = self.list(draft=draft)
        for ms in mss:
            if ignore_case:
                if ms.name.lower() == name.lower():
                    return ms
            else:
                if ms.name == name:
                    return ms

    def get_by_uuid(self,
                    uuid: str,
                    draft: bool = False):
        """Retrieve the Metadata Schema with the given uuid.

        :param uuid: the uuid of the metadata schema to retrieve
        :type path: str

        :param draft: if True, retrieves the draft of the Metadata Schema
        drafts, if any
        :type path: bool

        :return: the Metadata Schema or None
        :rtype: MetadataSchema
        """
        ms = self._fair_data_point.get(
            self.URL_PATH,
            uuid=uuid,
            drafts="true" if draft else "false")['content']

        if draft:
            _data = ms.get("draft", None)
        else:
            _data = ms.get("latest", None)

        if _data is None:
            return None

        _item = self.__class__(self._fair_data_point)
        _item._content_setter(_data)

        return _item

    def list(self, draft: bool = False):
        """Retrieve the list of all the Metadata Schemas.

        :param draft: if True, retrieves only the list of Metadata Schemas'
        drafts, if any
        :type path: bool

        :return: a list of the Metadata Schema
        :rtype: list[MetadataSchema]
        """
        ms_list = self._fair_data_point.get(
            self.URL_PATH,
            drafts="true" if draft else "false")['content']

        return_list = []

        for ms in ms_list:
            if draft:
                _data = ms.get("draft", None)
            else:
                _data = ms.get("latest", None)

            if _data is not None:
                _item = self.__class__(self._fair_data_point)
                _item._content_setter(_data)
                return_list.append(_item)

        return return_list
