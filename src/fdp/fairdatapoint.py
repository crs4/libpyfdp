import fdp.rest

from rdflib import Graph, Namespace

LDP = Namespace("http://www.w3.org/ns/ldp#")


class FairDataPoint(object):
    def __init__(self, url: str = 'http:/127.0.0.1', token: str = None):
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
    def uri(self) -> str:
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
            _c.read()
            _uuids[_uuid] = _c

        return _uuids

    def __str__(self):
        return f'<Fair Data Point client pointing to {self._url}>'
