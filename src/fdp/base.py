# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
from collections.abc import MutableSequence, MutableMapping
import json
import requests

import fdp

# from rdflib import Graph, URIRef
# from rdflib.namespace import DCTERMS


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class LibFDPError(RuntimeError):
    """Class for general LibFDP Errors."""
    def __init__(self, message):
        super().__init__(message)


class AlreadyPresentError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class NotPresentError(RuntimeError):
    def __init__(self, message=""):
        super().__init__(message)


class InstanceOverrideError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class IncompatibleClassError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class FairDataPointItem():
    """Base class for all the Fair Data Point entities."""

    _CLASS_PROPERTIES = []
    _CLASS_PROPERTIES_MAPPING = {}
    _CLASS_PROPERTIES_MAPPING_INVERTED = {}

    __frozen = False

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None):

        self._CLASS_PROPERTIES_MAPPING_INVERTED = {
            v: k for k, v in self._CLASS_PROPERTIES_MAPPING.items()}

        for _p in self._CLASS_PROPERTIES:
            setattr(self.__class__, f'_{_p}', None)

        self._fair_data_point = (fair_data_point or
                                 fdp.fairdatapoint.FairDataPoint('http://127.0.0.1'))
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
        return self._CLASS_PROPERTIES

    # def publish(self):
    #     raise NotImplementedError(
    #         "publish() method must be implemented in derived class.")

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

        response = self._fair_data_point.write(self.URL_PATH,
                                               payload=payload,
                                               headers=headers)

        self._uuid = response['content']['uuid']

        return response['content']

    def _get(self, uuid: str):
        element = self._fair_data_point.get(
            self.URL_PATH, uuid=uuid)['content']

        new_element = self.__class__(self._fair_data_point)

        for k in element:
            v = element[k]

            # Attribute exists but has a different name
            if k in self._CLASS_PROPERTIES_MAPPING_INVERTED:
                k = self._CLASS_PROPERTIES_MAPPING_INVERTED[k]

            if k in self._CLASS_PROPERTIES:
                if isinstance(v, (list, dict)):
                    func = getattr(new_element, f"add_{k}")
                    func(v)
                else:
                    setattr(new_element, k, v)
            elif k == 'uuid':
                setattr(new_element, '_uuid', v)
            # Unknow or not class-supported attribute
            # else:
            #     print(f"Unknown {k}")

        return new_element

    def _get_all(self):
        element_list = self._fair_data_point.get(self.URL_PATH)['content']

        for element in element_list:
            new_item = self.__class__()

            for k in element:
                v = element[k]

                # Attribute exists but has a different name
                if k in self._CLASS_PROPERTIES_MAPPING_INVERTED:
                    k = self._CLASS_PROPERTIES_MAPPING_INVERTED[k]

                if k in self._CLASS_PROPERTIES:
                    if isinstance(v, (list, dict)):
                        func = getattr(new_item, f"add_{k}")
                        func(v)
                    else:
                        setattr(new_item, k, v)
                elif k == 'uuid':
                    setattr(new_item, '_uuid', v)
                # Unknow or not class-supported attribute
                # else:
                #     print(f"Unknown {k}")
        return element_list

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
    def uuid(self) -> str:
        """The uuid attribute."""
        return self._uuid

    @property
    def fair_data_point(self):
        """The ``dcterms:isPartOf`` (Catalog's Fair Data Point) property."""
        return self._fair_data_point

    @fair_data_point.setter
    def fair_data_point(self, fair_data_point: str or
                        fdp.fairdatapoint.FairDataPoint):
        if isinstance(fair_data_point, str):
            self._fair_data_point = fdp.fairdatapoint.FairDataPoint(
                fair_data_point)
        elif isinstance(fair_data_point, fdp.fairdatapoint.FairDataPoint):
            self._fair_data_point = fair_data_point

    def create(self):
        """Creates a new Fair Data Point Item."""
        if self._uuid:
            raise LibFDPError(
                "The instance has an UUID: use update() function instead.")
        else:
            self._write()

    def delete(self):
        """Deletes a Fair Data Point Item from the Fair Data Point. On success, UUID
        attribute is set to None"""
        if self._uuid is None:
            raise LibFDPError(
                "The instance has no UUID.")
        else:
            self._delete()
            self._uuid = None

    def get(self, uuid):
        """Retrieves all the Fair Data Point Item of the derived class from the
        Fair Data Point."""
        return self._get(uuid)

    def get_all(self):
        """Retrieves all the Fair Data Point Item of the derived class from the
        Fair Data Point."""
        return self._get_all()

    def inspect(self):
        """Retrieves the value of the class properties.

        :return: a dictionary with the class's properties.
        :rtype: dict
        """
        return {_p: getattr(self, _p) for _p in self._CLASS_PROPERTIES}
