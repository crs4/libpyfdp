# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
import warnings

import fdp

from rdflib import Graph, Namespace

warnings.filterwarnings("ignore")

LDP = Namespace("http://www.w3.org/ns/ldp#")


class FairDataPoint():
    """Class representing a Fair Data Point.
    """
    def __init__(self, url: str = 'http://127.0.0.1', token: str = None):
        self._url = url
        self._rest_operator = fdp.rest.RestOperator(self._url, token)

    @property
    def rest_operator(self) -> str:
        """The rest_operator."""
        return self._rest_operator

    @rest_operator.setter
    def rest_operator(self, rest_operator: fdp.rest.RestOperator) -> None:
        self._rest_operator = rest_operator

    @property
    def url(self) -> str:
        """The uri of the Fair Data Point."""
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
            _c = fdp.catalog.Catalog(self, _iri)
            _c.read()                               # pylint: disable=no-member
            _uuids[_uuid] = _c

        return _uuids

    def __str__(self):
        return f'<Fair Data Point client pointing to {self._url}>'

    def write(self, path: str, payload: str, headers: dict or None):
        r = self._rest_operator.post(path,
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
        if isinstance(fairdatapointitem, fdp.base.FairDataPointItem):
            self._rest_operator.delete(fairdatapointitem.URL_PATH,
                                       fairdatapointitem.uuid)
        else:
            raise TypeError((f'Type {type(fairdatapointitem)} not allowed for '
                             '"delete" argument'))

    def get(self, path: str, uuid: str = None, **kwargs):
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
