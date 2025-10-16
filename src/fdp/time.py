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

# pylint: disable=unidiomatic-typecheck,invalid-name,missing-module-docstring
# pylint: disable=too-many-instance-attributes
import datetime

from rdflib import Literal, Graph, BNode
from rdflib.namespace import DCTERMS, DCAT, RDF

import fdp.fairdatapoint


class PeriodOfTime():
    """Class representing a DCATv3 dcat:PeriodOfTime.

    dcterms:PeriodOfTime represents an interval of time that is named or
    defined by its start and end dates.
    """

    _PERIODOFTIME_PROPERTIES = ['startDate', 'endDate']

    __frozen = False

    def __init__(self, fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
                 iri: str = None, uuid: str = None):
        for _p in self._PERIODOFTIME_PROPERTIES:
            setattr(PeriodOfTime, f'_{_p}', None)

        self._rdf = Graph()

        self._rdf.bind("dcat", DCAT)
        self._rdf.bind("dcterms", DCTERMS)

        self._uuid = uuid
        self._fair_data_point = fair_data_point or 'http://127.0.0.1'

        if iri is not None:
            # if type(iri) is str:
            #     self._iri = URIRef(iri)
            # elif type(iri) in [IdentifiedNode, URIRef, BNode]:
            #     self._iri = iri
            # else:
            raise TypeError((f'Type {type(iri)} not allowed for '
                             '"iri" argument'))
        # elif self._uuid is not None:
        #     self._iri = URIRef(
        #         f'{self._fair_data_point}/resource/{self._uuid}')
        # # XXX Check this
        # dataset_serie_distribution_iri = dataset_serie_iri + URIRef(
        #     f"/distribution/{house_name}.zip")
        else:
            self._iri = BNode()

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            DCTERMS.PeriodOfTime))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the PeriodOfTime instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the PeriodOfTime instance."""
        return self._rdf

    @property
    def tainted(self) -> bool:
        """Whether the instance has been modified after creation/sync with the
        Fair Data Point."""
        return self._tainted

    @property
    def startDate(self):
        """ The ``dcat:startDate`` property."""
        return self._startDate

    @startDate.setter
    def startDate(self, startDate: datetime.datetime or str):
        if type(startDate) in [datetime.datetime, datetime.date]:
            self._startDate = startDate
        elif type(startDate) is str:
            self._startDate = datetime.datetime.fromisoformat(startDate)
        else:
            raise TypeError(("startDate property must be a datetime.datetime "
                             "class instance or a string in the "
                             "format\"YYYY-MM-DDTHH:MM:SSTZ\"."))

        self._rdf.add((
            self._iri,
            DCAT.startDate,
            Literal(self._startDate)
        ))

        self._tainted = True

    @property
    def endDate(self):
        """ The ``dcat:endDate`` property."""
        return self._endDate

    @endDate.setter
    def endDate(self, endDate: datetime.datetime or str):
        if type(endDate) in [datetime.datetime, datetime.date]:
            self._endDate = endDate
        elif type(endDate) is str:
            self._endDate = datetime.datetime.fromisoformat(endDate)
        else:
            raise TypeError(("endDate property must be a datetime.datetime "
                             "class instance or a string in the "
                             "format\"YYYY-MM-DDTHH:MM:SSTZ\"."))

        self._rdf.add((
            self._iri,
            DCAT.endDate,
            Literal(self._endDate)
        ))

        self._tainted = True
