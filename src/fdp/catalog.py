import datetime

from rdflib import Graph, URIRef, Literal, BNode, IdentifiedNode
from rdflib.namespace import DCAT, DCTERMS, FOAF, RDF  # , XSD, SKOS

import fdp.fairdatapoint
import fdp.version
from .base import InstanceOverrideError


class Catalog(object):
    """Class representing a DCATv3 Catalog.

    :var uuid: the uuid that is assigned by the Fair Data Point
    :vartype uuid: str
    """

    _PROPERTIES = ['creator', 'description', 'homepage', 'issued', 'license',
                   'publisher', 'title', 'version']

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 iri: str = None, uuid: str = None):
        self._uuid = uuid
        self._fair_data_point = fair_data_point or None

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError((f'Type {type(iri)} not allowed for '
                                 '"iri" argument'))
        elif self._uuid is not None:
            self._iri = URIRef(f'{self._fair_data_point}/catalog/{self._uuid}')
        else:
            self._iri = BNode()

        self._tainted = False

        self._creator = None
        self._description = None
        self._homepage = None
        self._issued = None
        self._license = None
        self._publisher = None
        self._title = None
        self._version = fdp.version.Version()

        self._rdf = Graph()

        self._rdf.bind("dcat", DCAT)
        self._rdf.bind("dcterms", DCTERMS)
        self._rdf.bind("foaf", FOAF)

        self._rdf.add((
            self._iri,
            RDF.type,
            DCAT.Catalog))

        self._rdf.add((
            self._iri,
            RDF.type,
            DCAT.Resource))

        if self._fair_data_point:
            self._rdf.add((
                self._iri,
                DCTERMS.isPartOf,
                URIRef(self._fair_data_point.url)))

    ###########################################################################
    # DCATv3 Class properties                                                 #
    ###########################################################################
    @property
    def creator(self):
        """The ``dcterms:creator`` property."""
        return self._creator

    # XXX if creator is a list it must be a Group
    # while a str should be used for Person
    @creator.setter
    def creator(self, creator: str or list):
        self._creator = creator

        _cc = BNode()
        self._rdf.add((URIRef(self._iri), DCTERMS.creator, _cc))
        self._rdf.add((_cc, RDF.type, FOAF.Group))

        _ccm = BNode()
        self._rdf.add((_cc, FOAF.member, _ccm))
        self._rdf.add((_ccm, RDF.type, FOAF.Person))

        if isinstance(self._creator, list):
            for _c in self._creator:
                if isinstance(_c, str):
                    self._rdf.add((_ccm, FOAF.name, Literal(_c)))
        elif isinstance(self._creator, str):
            self._rdf.add((_ccm, FOAF.name, Literal(self._creator)))

        self._tainted = True

    @property
    def description(self):
        """The ``dcterms:description`` property."""
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description
        self._rdf.add((
            URIRef(self._iri),
            DCTERMS.description,
            Literal(self._description)))

        self._tainted = True

    @property
    def homepage(self):
        """The ``foaf:homepage`` property."""
        return self._homepage

    @homepage.setter
    def homepage(self, homepage: str):
        self._homepage = homepage
        self._rdf.add((
            URIRef(self._iri),
            FOAF.homepage,
            URIRef(homepage)))

        self._tainted = True

    @property
    def issued(self):
        """ The ``dcterms:issued`` property."""
        return self._issued

    @issued.setter
    def issued(self, issued: datetime.datetime or str):
        if isinstance(issued, datetime.datetime):
            self._issued = issued
        elif isinstance(issued, str):
            self._issued = datetime.strptime(issued, '%Y-%m-%dT%H:%M:%S%z')
        else:
            raise ValueError(("issue property must be a datetime.datetime "
                              "class instance or a string in the "
                              "format\"YYYY-MM-DDTHH:MM:SSTZ\"."))

        self._rdf.add((URIRef(self._iri), DCTERMS.issued,
                       Literal(self._issued)))

        self._tainted = True

    @property
    def license(self):
        """The ``dcterms:license`` property."""
        return self._license

    @license.setter
    def license(self, license: str):
        self._license = license
        self._rdf.add((
            URIRef(self._iri),
            DCTERMS.license,
            URIRef(self._license)))

        self._tainted = True

    @property
    def publisher(self):
        """The ``dcterms:publisher`` property."""
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str or dict or fdp.FOAFAgent):
        if isinstance(publisher, str):
            self._publisher = fdp.foaf.FOAFAgent(dictionary={
                'type': 'Person',
                'name': publisher
            })
            self._rdf += self._publisher.rdf
            self._tainted = True
        elif isinstance(publisher, fdp.foaf.FOAFAgent):
            self._publisher = publisher
            self._rdf += self._publisher.rdf
            self._tainted = True
        elif isinstance(publisher, dict):
            self._publisher = fdp.foaf.FOAFAgent(dictionary=publisher)
            self._rdf += self._publisher.graph
            self._rdf.add((URIRef(self._iri), DCTERMS.publisher,
                           self._publisher.agent))
            self._tainted = True
        else:
            raise ValueError(("publisher must be a FOAFAgent's class instance "
                              "or a string in the format or a dictionary."))
        self._rdf.add((URIRef(self._iri), DCTERMS.publisher,
                       self._publisher.iri))

    @property
    def title(self):
        """The ``dcterms:title`` property."""
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
        self._rdf.add((
            URIRef(self._iri),
            DCTERMS.title,
            Literal(self._title)))

        self._tainted = True

    @property
    def version(self):
        """The ``dcat:version`` property."""
        return self._version

    @version.setter
    def version(self, version: str or fdp.version.Version or int):
        if isinstance(version, str):
            self._version = fdp.version.Version(version=version)
        elif isinstance(version, fdp.version.Version):
            self._version = version
        elif isinstance(version, int):
            self._version = fdp.version.Version(
                major=version, minor=0, patch=0)
        else:
            raise ValueError("version must be a Version's class instance or a "
                             "string in the format \"major.minor.patch\", "
                             "e.g. \"1.0.0\".")
        self._rdf.add((
            URIRef(self._iri),
            DCAT.version,
            Literal(self._version.as_str())))

        self._tainted = True

    ###########################################################################

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

        self._rdf.add((
            URIRef(self._iri),
            DCTERMS.isPartOf,
            URIRef(self._fair_data_point.url)))

    @property
    def iri(self):
        """The iri of the Catalog instance."""
        return self._iri

    @property
    def properties(self):
        """The DCATv3 Catalog class properties available.

        :returns: a list of the Catalog class properties available.
        :rtype: list of str
        """
        return self._PROPERTIES

    @property
    def rest_operator(self) -> str:
        """The rest_operator."""
        return self._fair_data_point._rest_operator

    @property
    def uuid(self):
        """The uuid assigned to the Catalog instance by the Fair Data Point."""
        return self._uuid

    def rdf(self) -> str:
        """Returns the string representing the DCATv3 Catalog instance in
        rdf/turtle format.

        :returns: the rdf/turtle representation of the Catalog instance.
        :rtype: str
        """
        return self._rdf.serialize()

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

        if self._iri:
            r = self._fair_data_point._rest_operator.get(
                self._iri, absolute=True)

            self._rdf = Graph().parse(data=r['content'])

            # Creator is a foaf:Agent, e.g. foaf:Group or foaf:Person
            _creator = self._rdf.value(subject=self._iri,
                                       predicate=DCTERMS.creator,
                                       any=False)

            # XXX Could it be done better with metaclasses?
            if _creator is not None:
                _creator = fdp.foaf.FOAFFactory().get_agent(
                    self._rdf.cbd(_creator))

            # Creator is a foaf:Agent, e.g. foaf:Group or foaf:Person
            # _creator = self._rdf.value(subject=self._iri,
            #                            predicate=DCTERMS.creator, any=False)
            # _creator_agent = self._rdf.value(
            #     subject=_creator, predicate=RDF.type
            # ).n3(self._rdf.namespace_manager)

            # _creator_list = []
            # _creator should consider also Person and Agent types
            # if _creator_agent == "foaf:Group":
            #     _creator_member = self._rdf.value(subject=_creator,
            #                                       predicate=FOAF.member,
            #                                       any=False)

            #     for person in self._rdf.objects(_creator_member, FOAF.name):
            #         _creator_list.append(str(person))

            _description = self._rdf.value(subject=self._iri,
                                           predicate=DCTERMS.description,
                                           any=False)

            _homepage = self._rdf.value(subject=self._iri,
                                        predicate=FOAF.homepage,
                                        any=False)

            _issued = self._rdf.value(self._iri,
                                      predicate=DCTERMS.issued,
                                      any=False)

            # XXX license could be a list?
            _license = list(self._rdf.objects(None, DCTERMS.license))[0]

            _title = self._rdf.value(self._iri,
                                     predicate=DCTERMS.title,
                                     any=False)

            _version = self._rdf.value(self._iri,
                                       predicate=DCAT.version,
                                       any=False)

            _publisher = self._rdf.value(subject=self._iri,
                                         predicate=DCTERMS.publisher,
                                         any=False)

            # XXX Could it be done better with metaclasses?
            _publisher = fdp.foaf.FOAFFactory().get_agent(
                self._rdf.cbd(_publisher))

            # self._creator = _creator_list
            self._creator = _creator
            self._description = str(_description)
            self._homepage = str(_homepage)
            self._issued = datetime.datetime.fromisoformat(str(_issued))
            self._license = str(_license)
            self._publisher = str(_publisher)
            self._title = str(_title)
            self._version = fdp.version.Version(str(_version))

        if self._uuid:
            # if drafts:
            r = self._fair_data_point._rest_operator.get(
                f'catalog/{self._uuid}/draft')
            self._schema = r['content']
    #             self._version = Version(self._schema['lastVersion'])
    #         else:
    #             r = self._rest_operator.get(
    #                 f'metadata-schemas/{self._uuid}', raise_for_status=False)
    #             if r['code'] >= 400:
    #                 return
    #             self._schema = r['content']
    #             self._version = Version(self._schema['version'])
    #     elif self._name:
    #         parameters = {'drafts': drafts}

    #         r = self._rest_operator.get('metadata-schemas',
    #                                     parameters=parameters)
    #         schemas = [i for i in r['content'] if self._name in i['name']]
    #         # If there are more than one Metadata Schema with the same name
    #         # only the first one returned from the FDP is used.
    #         if len(schemas) > 0:
    #             if drafts:
    #                 self._schema = schemas[0]['draft']
    #                 self._version = Version(self._schema['lastVersion'])
    #             else:
    #                 self._schema = schemas[0]['latest']
    #                 self._version = Version(self._schema['version'])
        else:
            return

        self._uuid = self._schema['uuid']
        self._description = self._schema['description']
        self._definition = self._schema['definition']

    def write(self, allow_update: bool = True, allow_duplicates: bool = False):
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
        # uuids = self.find(self._title)
        # uuids = None

        headers = {
            'Content-Type': 'text/turtle',
        }

        if self._uuid is None or allow_duplicates:
            r = self._fair_data_point._rest_operator.post('catalog',
                                                          headers=headers,
                                                          payload=self.rdf)
            _rdf = Graph().parse(data=r['content'])
            self._uuid = list(
                _rdf.objects(None, DCTERMS.identifier, unique=True))[0]
            self._uuid = self._uuid.rpartition('/')[2]

        # elif allow_update:
        #     r = self._rest_operator.put(f'metadata-schemas/{uuids[0]}/draft',
        #                                 payload=self.payload)
        #     self._uuid = r['content']['uuid']
        # else:
        #     raise AlreadyPresentError(
        #         (f"Metadata schema \"{self.name}\" already present "
        #           "in the Fair Data Point."))

    def inspect(self):
        """Retrieves the value of the class properties.

        :return: a dictionary with the class's properties.
        :rtype: dict
        """
        return {_p: getattr(self, _p) for _p in self._PROPERTIES}

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    def __str__(self):
        return (f"<Catalog uuid={self._uuid}, title=\'{self._title}\', "
                f"version={self._version}, "
                "{}>".format("Tainted" if self._tainted else "NotTainted"))
