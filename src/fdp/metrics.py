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

from rdflib import URIRef, Literal, Graph, BNode, IdentifiedNode
from rdflib.namespace import XSD, RDF, Namespace, SKOS, NamespaceManager

DQV = Namespace("http://www.w3.org/ns/dqv#")
LDQD = Namespace("https://www.w3.org/2016/05/ldqd#")
LOCAL = Namespace("#")


class DatasetDensityMetric():
    """Class representing the completeness dataset density metric in
    timeseries."""

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        self._rdf = Graph()

        # self._rdf.namespace_manager = NamespaceManager(Graph())
        # self._rdf.namespace_manager.bind('', LOCAL)

        self._rdf.bind("dqv", DQV)
        self._rdf.bind("skos", SKOS)
        self._rdf.bind("ldqd", LDQD)
        self._rdf.bind("", LOCAL)

        self._uuid = uuid

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError((f'Type {type(iri)} not allowed for '
                                 '"iri" argument'))
        # elif self._uuid is not None:
        #     self._iri = URIRef(
        #         f'{self._fair_data_point}/resource/{self._uuid}')
        # # XXX Check this
        # dataset_serie_distribution_iri = dataset_serie_iri + URIRef(
        #     f"/distribution/{house_name}.zip")
        else:
            self._iri = LOCAL['dataDensityMetric']

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            DQV.Metric))

        self._rdf.add((
            self._iri,
            SKOS.definition,
            Literal(
              "Ratio between the number of objects represented in the "
              "dataset and the number of objects expected to be "
              "represented according to the declared staring time, "
              "ending time and frequency.", lang='en')))

        self._rdf.add((
            self._iri,
            DQV.expectedDataType,
            XSD.double))

        # dataset_density_dimension = URIRef(":dataDensityDimension")
        # point_density_dimension = PointDensityDimension()

        self._rdf.add((
            self._iri,
            DQV.inDimension,
            LDQD.completeness))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the DatasetDensityMetric instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the DatasetDensityMetric instance."""
        return self._rdf


class CompletenessMeasurement():
    """Class representing a DQV Measurement."""

    _DQVMEASUREMENT_PROPERTIES = ['isMeasurementOf', 'value']

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        for _p in self._DQVMEASUREMENT_PROPERTIES:
            setattr(CompletenessMeasurement, f'_{_p}', None)

        self._rdf = Graph()
        self._rdf.bind("dqv", DQV)
        self._rdf.bind("ldqd", LDQD)
        self._rdf.bind("", LOCAL)

        self._uuid = uuid

        if iri is not None:
            if type(iri) is str:
                self._iri = URIRef(iri)
            elif type(iri) in [IdentifiedNode, URIRef, BNode]:
                self._iri = iri
            else:
                raise TypeError((f'Type {type(iri)} not allowed for '
                                 '"iri" argument'))
        elif self._uuid is not None:
            self._iri = URIRef(
                f'{self._fair_data_point}/resource/{self._uuid}')
        else:
            # self._iri = BNode()
            self._iri = LOCAL['DatasetCompletenessMeasurement']

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            DQV.QualityMeasurement
        ))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the CompletenessMeasurement instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the CompletenessMeasurement instance."""
        return self._rdf

    @property
    def isMeasurementOf(self) -> dict:
        """The associated metric to the Completeness Measurement."""
        return self._isMeasurementOf

    @isMeasurementOf.setter
    def isMeasurementOf(self, metric: DatasetDensityMetric):
        if isinstance(metric, DatasetDensityMetric):
            self._isMeasurementOf = metric
            self._rdf += self._isMeasurementOf.rdf

            self._tainted = True
        else:
            raise TypeError(
                ("isMeasurementOf must be a DatasetDensityMetric's "
                 "class instance"))

        self._rdf.add((
            self._iri,
            DQV.isMeasurementOf,
            self._isMeasurementOf.iri
        ))

    @property
    def value(self) -> dict:
        """The value of the Measurement."""
        return self._value

    @value.setter
    def value(self, value: float or int or Literal):
        if isinstance(value, float):
            self._value = value
            self._tainted = True
        elif isinstance(value, int):
            self._value = float(value)
            self._tainted = True
        elif isinstance(value, Literal) and value.datatype == XSD.float:
            self._value = float(value)
            self._tainted = True
        else:
            raise TypeError(("value must be a float, int or a Literal's "
                             "class instance of type XSD:float"))
        self._rdf.add((
            self._iri,
            DQV.value,
            Literal(self._value, datatype=XSD.float)
        ))
