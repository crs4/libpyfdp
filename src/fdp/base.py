from .rest import RestOperator
from .version import Version


class AlreadyPresentError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class NotPresentError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class InstanceOverrideError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class FairDataPointItem(object):
    """Base class for all the Fair Data Point entities."""
    def __init__(self):
        pass

    def publish(self):
        raise NotImplementedError(
            "publish() method must be implemented in derived class.")

    def write(self, allow_update: bool = True, allow_duplicates: bool = False):
        raise NotImplementedError(
            "write() method must be implemented in derived class.")

    def read(self, drafts: bool = False, override: bool = False):
        raise NotImplementedError(
            "read() method must be implemented in derived class.")


class MetadataSchema(FairDataPointItem):
    """Base class for all the Fair Data Point Metadata Schema."""
    def __init__(self, name: str = None, description: str = None,
                 definition: str = None,
                 rest_operator: RestOperator = None):
        self._name = name or None
        self._description = description or None
        self._definition = definition or None
        self._uuid = None
        self._version = None
        self._tainted = False
        self._schema = None
        self._rest_operator = rest_operator

    @property
    def name(self) -> str:
        """The name attribute."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        self._tainted = True

    @property
    def description(self) -> str:
        """The description attribute."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description
        self._tainted = True

    @property
    def definition(self) -> str:
        """The definition attribute."""
        return self._definition

    @definition.setter
    def definition(self, definition: str) -> None:
        self._definition = definition
        self._tainted = True

    @property
    def tainted(self) -> str:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def uuid(self) -> str:
        """The uuid attribute."""
        return self._uuid

    @property
    def rest_operator(self) -> str:
        """The rest_operator."""
        return self._rest_operator

    @rest_operator.setter
    def rest_operator(self, rest_operator: RestOperator) -> None:
        self._rest_operator = rest_operator

    @property
    def version(self) -> str:
        """The version attribute."""
        return self._version

    @version.setter
    def version(self, version: str or Version) -> str:
        """The version attribute."""
        if isinstance(version, str):
            self._version = Version(version)
        elif isinstance(version, Version):
            self._version = version
        else:
            raise ValueError

    def check_duplicates(self, schema_name: str) -> list:
        """Checks if a metadata schema is already present in the FDP.

        :param schema_name: the name of the schema to check
        :type schema_name: str

        :return: a list of uuids of the metadata schemas found having the same
                 name or None
        :rtype: list or None
        """
        parameters = {'drafts': True}

        r = self._rest_operator.get('metadata-schemas', parameters=parameters)
        uuids = [i['uuid'] for i in r['content'] if schema_name in i['name']]

        return None if len(uuids) == 0 else uuids

    def write(self, allow_update: bool = True, allow_duplicates: bool = False):
        """Writes the instance attributes to the Fair Data Point.

        :param allow_update: if true, override the instance's attribute;
        :type allow_update: bool

        :param allow_duplicates: write the Metadata Schema even if there are
                                  other schemas with the same name.
        :type allow_duplicates: bool

        :raises AlreadyPresentError: if the schema already exists in the Fair
                                     Data Point and allow_duplicates is not
                                     set.

        .. note::
            a property called 'payload' that returns a dictionary with the
            attributes must be implemented.
        """
        uuids = self.check_duplicates(self.name)

        if uuids is None or allow_duplicates:
            r = self._rest_operator.post('metadata-schemas',
                                         payload=self.payload)
            self._uuid = r['content']['uuid']
        elif allow_update:
            r = self._rest_operator.put(f'metadata-schemas/{uuids[0]}/draft',
                                        payload=self.payload)
            self._uuid = r['content']['uuid']
        else:
            raise AlreadyPresentError(
                (f"Metadata schema \"{self.name}\" already present "
                  "in the Fair Data Point."))

    def read(self, drafts: bool = False, override: bool = False):
        """Populates the instance attributes with data read from the Fair Data
        Point.

        :param drafts: if true, retrieves also the drafts, if any
        :type drafts: bool

        :param override: if set the read will override the attributes,
                             raise an InstanceOverrideError error instead
                             if the instance ha been modified but not
                             written back (it is 'tainted').
        :type override: bool

        :raises InstanceOverrideError: if the instance is tainted.
        """

        if self._tainted and not override:
            raise InstanceOverrideError(
                ("The instance is tainted. Any attempt to read the attributes "
                 "of the Metadata Schema from the Fair Data Point will "
                 "overwrite your modifications."))

        if self._uuid:
            if drafts:
                r = self._rest_operator.get(
                    f'metadata-schemas/{self._uuid}/draft')
                self._schema = r['content']
                self._version = Version(self._schema['lastVersion'])
            else:
                r = self._rest_operator.get(
                    f'metadata-schemas/{self._uuid}', raise_for_status=False)
                if r['code'] >= 400:
                    return
                self._schema = r['content']
                self._version = Version(self._schema['version'])
        elif self._name:
            parameters = {'drafts': drafts}

            r = self._rest_operator.get('metadata-schemas',
                                        parameters=parameters)
            schemas = [i for i in r['content'] if self._name in i['name']]
            # If there are more than one Metadata Schema with the same name
            # only the first one returned from the FDP is used.
            if len(schemas) > 0:
                if drafts:
                    self._schema = schemas[0]['draft']
                    self._version = Version(self._schema['lastVersion'])
                else:
                    self._schema = schemas[0]['latest']
                    self._version = Version(self._schema['version'])
        else:
            return

        self._uuid = self._schema['uuid']
        self._description = self._schema['description']
        self._definition = self._schema['definition']

    def publish(self):
        if self._uuid is None:
            raise NotPresentError((
                "Attempting to publish a Metadata Schema that does not exist. "
                "Metadata Schema must be present in the Fair Data Point to be "
                "published."))

        payload = {
            "version": self._version.as_str(),
            "description": self.description,
            # "published": "true"
        }

        _ = self._rest_operator.post(f'metadata-schemas/{self._uuid}/versions',
                                     payload=payload)

    def __str__(self):
        return (f"<MetadataSchema uuid={self._uuid}, name=\"{self._name}\", "
                f"version={self._version}, "
                "{}>".format("Tainted" if self._tainted else "NotTainted"))
