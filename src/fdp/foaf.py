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

"""
FOAF Module
====================

This module provides Python classes representing **FOAF (Friend of a Friend)
entities**.  These classes allow modeling agents, people, groups, and
organizations with their commonly used FOAF properties in an RDF graph or other
semantic applications.

Classes
-------

- :class:`FOAFAgent`
  The most general FOAF entity. Can represent any actor such as a person,
  group, or organization.  Supports properties such as `foaf:name`,
  `foaf:homepage`, `foaf:knows`, `foaf:depiction`, etc.

- :class:`FOAFPerson`
  Represents an individual human being. Inherits from :class:`Agent`.  Supports
  properties like `foaf:firstName`, `foaf:lastName`, `foaf:nick`, `foaf:img`,
  `foaf:knows`, etc.

- :class:`FOAFGroup`
  Represents a collection of people, such as a team, club, or association.
  Inherits from :class:`Agent`.  Supports properties such as `foaf:member`,
  `foaf:homepage`, `foaf:logo`, etc.

- :class:`FOAFOrganization`
  Represents an organization such as a company, institution, or agency.
  Inherits from :class:`Agent`.  Supports properties like `foaf:member`,
  `foaf:homepage`, `foaf:logo`, `foaf:fundedBy`, etc.

Usage
-----

You can import the classes and create instances representing FOAF entities:

.. code-block:: python

    import fdp

    # create a foaf:Person entity
    alice = fdp.foaf.FOAFPerson()

    # add details to the Person
    alice.name = 'Alice'
    alice.homepage = 'https://www.example.com/alice'

    # create a foaf:Group entity
    team = fdp.foaf.FOAFGroup()

    # add details to the Group
    team.name = 'A Team'
    team.homepage = 'https://www.example.com/a-team'

    # add Alice to the group
    team.add_member(alice)

    # create a Sofia foaf:Person and add to the group
    team.add_member(
        fdp.foaf.FOAFPerson(name='Sofia',
                            homepage='https://www.example.com/sofia'))

    # inspect the Group
    import pprint
    pprint.pprint(team.inspect())

    # retrieve the Group's rdf graph
    team_graph = team.rdf

    # pretty print the Group's rdf graph
    print(team_graph.serialize())

    # create a team with details
    new_team = fdp.foaf.FOAFGroup(
        name='B-Team',
        homepage='https://www.example.com/b-team',
        member=[
            fdp.foaf.FOAFPerson(
                name='Mario',
                homepage='https://www.example.com/mario'),
            fdp.foaf.FOAFPerson(
                name='Marco',
                homepage='https://www.example.com/marco')
        ])
"""

from __future__ import annotations

from rdflib import Graph, BNode, Literal, URIRef, IdentifiedNode
from rdflib.namespace import FOAF, RDF
import fdp
from fdp.fairdatapointitem import FairDataPointItem


class FOAFFactory:
    _SUPPORTED_CLASSES = ['foaf:Agent', 'foaf:Group', 'foaf:Organization',
                          'foaf:Person']

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint):
        self._fair_data_point = fair_data_point

    def get_agent(self, rdf_graph: Graph):
        for s, p, o in rdf_graph.triples((None,  RDF.type, None)):
            if o == FOAF.Agent:
                return fdp.foaf.FOAFAgent(self._fair_data_point, s)
                # p._content_setter(rdf_graph.cbd(s))
            elif o == FOAF.Person:
                return fdp.foaf.FOAFPerson(self._fair_data_point, s)
                # p._content_setter(rdf_graph.cbd(s))
            elif o == FOAF.Group:
                return fdp.foaf.FOAFGroup(self._fair_data_point, s)
                # p._content_setter(rdf_graph.cbd(s))
            elif o == FOAF.Organization:
                return fdp.foaf.FOAFOrganization(self._fair_data_point, s)


class FOAFAgent(FairDataPointItem):
    """
    A class representing a FOAF Agent.

    The most general FOAF entity: represents anything that can act (e.g., a
    person, group, or organization).
    All other FOAF entities inherit from Agent.

    Supported FOAF properties:
      - name
      - homepage
      - members
    """

    # _SUPPORTED_PROPERTIES = ['foaf:homepage', 'foaf:name', 'foaf:member']
    _WRITE_PROPERTIES = [
        "name",
        "homepage",
        "member",
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    _FOAF_CLASS = FOAF.Agent

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
        *args,
        **kwargs,
    ):

        super().__init__(fair_data_point)

        self._rdf = Graph()

        self._uuid = uuid

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError(
                    (f"Type {type(iri)} not allowed for " '"iri" argument')
                )
        elif self._uuid is not None:
            self._iri = URIRef(
                f"{self._fair_data_point.url}/resource/{self._uuid}"
            )
        else:
            self._iri = BNode()

        self._tainted = False

        self._rdf.add((self._iri, RDF.type, FOAF.Agent))

        for _p, _v in kwargs.items():
            if _p in self._WRITE_PROPERTIES:
                if hasattr(self, f"add_{_p}"):
                    func = getattr(self, f"add_{_p}")
                    func(_v)
                else:
                    getattr(type(self), _p).fset(self, _v)

    @property
    def iri(self):
        return self._iri

    @property
    def rdf(self):
        return self._rdf

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def homepage(self):
        """
        The ``foaf:homepage`` property.

        The property can be read or updated. When setting the value, several
        input types are accepted:

        * a plain string containing the URL (e.g., ``"https://example.org"``)
        * an :class:`rdflib.term.Literal` representing a URL
        * an :class:`rdflib.term.URIRef` instance
        * an :class:`rdflib.graph.Graph` containing one or more
          ``foaf:homepage`` triples

        .. warning::
           If a graph is provided either as the value or via the namespace, and
           it contains multiple ``foaf:homepage`` triples, **only the first one
           encountered is used**.

        :type: str | rdflib.term.Literal | rdflib.term.URIRef
        :rtype: str
        :return: The homepage URL of the entity as a string.
        :raises ValueError: If the value cannot be converted to a valid URL.
        """
        return self._homepage

    @homepage.setter
    def homepage(self, homepage: str | Literal | URIRef | Graph):
        if type(homepage) is Graph:
            _subject = homepage.value(None, RDF.type, self._FOAF_CLASS,
                                      any=False)
            homepage = homepage.value(_subject, FOAF.homepage, any=False)

        if homepage is None:
            return
        elif type(homepage) is str:
            self._homepage = homepage
        elif type(homepage) is Literal:
            self._homepage = str(homepage)
        elif type(homepage) is URIRef:
            self._homepage = str(homepage)
        else:
            ValueError("Homepage must be a string, Literal, or URIRef.")

        self._rdf.add((
            self._iri,
            FOAF.homepage,
            URIRef(self._homepage)))

        self._tainted = True

    @property
    def name(self):
        """
        The ``foaf:name`` property.

        The property can be read or updated.
        When setting the value, several input types are accepted:

        * a plain string (e.g., ``"Alice Smith"``)
        * an :class:`rdflib.term.Literal` representing a name
        * an :class:`rdflib.graph.Graph` containing one or more ``foaf:name``
          triples

        .. warning::
           If a graph contains multiple ``foaf:name`` triples, **only the first
           one encountered is used**.

        :type: str | rdflib.term.Literal | rdflib.graph.Graph
        :rtype: str
        :return: The name of the entity as a string.
        :raises ValueError: If the value cannot be converted to a valid name.
        """
        return self._name

    @name.setter
    def name(self, name: str or Literal or Graph):
        if type(name) is Graph:
            _subject = name.value(None, RDF.type, self._FOAF_CLASS, any=False)
            name = name.value(_subject, FOAF.name, any=False)

        if name is None:
            return
        elif type(name) is str:
            self._name = name
        elif type(name) is Literal:
            self._name = str(name)
        else:
            raise ValueError("Name must be a string, Literal or Graph.")

        self._rdf.add((
            self._iri,
            FOAF.name,
            Literal(self._name)))

        self._tainted = True

    @property
    def member(self) -> dict:
        """
        The ``foaf:member`` property.

        The setter for this property is the function ``add_member``.
        """
        return self._member

    def add_member(self, member: FOAFAgent | Graph | list[FOAFAgent]) -> None:
        """
        Add one or more members.

        This function accepts either a single :class:`FOAFAgent` instance (or
        any of its subclasses), an :class:`rdflib.graph.Graph` object
        containing agent data, or a list of :class:`FOAFAgent` instances (or
        subclasses).  The provided member(s) are added to the instance RDF
        graph, creating the corresponding RDF triples as needed.

        :param member: The member or members to add.
                       It can be one of the following:

                       - An :class:`FOAFAgent` instance or subclass
                       - An :class:`rdflib.graph.Graph` instance
                       - A list of :class:`FOAFAgent` instances or subclasses
        :type member: FOAFAgent | rdflib.Graph | list[FOAFAgent]
        :return: None
        :rtype: None
        :raises TypeError: If the input type is not supported.

        .. note::
            - When a list is provided, each element must be an instance of
                :class:`FOAFAgent` or one of its subclasses.
            - When a :class:`rdflib.graph.Graph` is provided and it contains
                more than one member description, **all members** found in the
                graph are added.
        """
        if member is None:
            return

        if self._member is None:
            self._member = {}

        _member_list = []

        if isinstance(member, Graph):
            for member_iri in member.objects(None, FOAF.member):
                member_graph = member.cbd(member_iri)

                _m = FOAFFactory(
                    self._fair_data_point).get_agent(member_graph)
                _m._content_setter(member_graph)

                _member_list.append(_m)
        elif isinstance(member, FOAFAgent):
            _member_list.append(member)
        elif isinstance(member, list):
            for _m in member:
                _member_list.append(_m)
        else:
            raise TypeError((f"Type {type(member)} is not valid for "
                             "\"add_member()\" argument"))

        for _m in _member_list:
            self._member.update({_m.iri: _m})

            self._rdf.add((
                self._iri,
                FOAF.member,
                _m.iri
            ))

            self._rdf += _m.rdf

    def __str__(self):
        return (f"<{self.__class__.__module__}.{self.__class__.__name__}"
                f", iri: {self._iri}"
                "{}".format(f", name: {self._name}>" if self._name is not None
                            else ">"))

    def _content_setter(self, rdf):
        for _p in self._WRITE_PROPERTIES:
            if hasattr(self, f"add_{_p}"):
                func = getattr(self, f"add_{_p}")
                func(rdf)
            else:
                getattr(type(self), _p).fset(self, rdf)


class FOAFPerson(FOAFAgent):
    """
    A class representing a FOAF Person.

    Represents an individual human being. Inherits from :class:`Agent`.

    Supported FOAF properties:
      - name
      - homepage
    """

    _WRITE_PROPERTIES = [
        "name",
        "homepage",
        # firstName
        # lastName
        # mbox
        # nick
        # img
        # depiction
        # knows
        # gender
        # age
        # based_near
        # interest
        # topic_interest
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    _FOAF_CLASS = FOAF.Person

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(fair_data_point, iri, uuid, *args, **kwargs)

        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Person))

    # def add_member(self, member: FOAFAgent):
    #     raise NotImplementedError

    # @property
    # def members(self) -> dict:
    #     """Method not available for FOAF Person."""
    #     raise NotImplementedError


class FOAFOrganization(FOAFAgent):
    """
    A class representing a FOAF Organization.

    Represents an organization such as a company, institution, or agency.
    Inherits from :class:`Agent`.

    Supported FOAF properties:
      - name
      - member
      - homepage
    """

    _WRITE_PROPERTIES = [
        "name",
        "homepage",
        "member",
        # depiction
        # based_near
        # logo
        # fundedBy
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    _FOAF_CLASS = FOAF.Organization

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(fair_data_point, iri, uuid, *args, **kwargs)
        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Organization
        ))


class FOAFGroup(FOAFAgent):
    """
    A class representing a FOAF Group.

    Represents a collection of people, e.g., a team or club. Inherits from
    :class:`Agent`.

    Supported FOAF properties:
      - name
      - member
      - homepage
    """

    _WRITE_PROPERTIES = [
        "name",
        "homepage",
        "member",
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    _FOAF_CLASS = FOAF.Group

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(fair_data_point, iri, uuid, *args, **kwargs)
        self._rdf.set((
            self._iri,
            RDF.type,
            FOAF.Group
        ))
