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
from rdflib import Graph
from rdflib.namespace import DCAT, DCTERMS, RDF, Namespace
from rdflib.term import URIRef, IdentifiedNode

import fdp.fairdatapoint
from fdp.resource import Resource
from fdp.distribution import Distribution
from fdp.time import PeriodOfTime
from fdp.metrics import CompletenessMeasurement

DQV = Namespace("http://www.w3.org/ns/dqv#")
SPDX = Namespace("http://spdx.org/rdf/terms#")
LDQD = Namespace("https://www.w3.org/2016/05/ldqd#")


class Dataset(Resource):
    """
    Class representing a DCATv3 :class:`dcat:Dataset` entity.

    A **Dataset** is a collection of data available for access or download in
    one or more distributions.

    This class extends :class:`fdp.resource.Resource`.

    **RDF Class**
        ``dcat:Dataset``

    **Base Classes**
        - :class:`fdp.resource.Resource`

    **Supported inherited properties**
        From :class:`Resource`:
            - :attr:`creator`
            - :attr:`description`
            - :attr:`issued`
            - :attr:`license`
            - :attr:`publisher`
            - :attr:`theme`
            - :attr:`title`
            - :attr:`version`

    **Supported Dataset-specific properties**
        - :attr:`hasQualityMeasurement` — quality metrics associated with the dataset
        - :attr:`inSeries` — links the dataset to a parent :class:`DatasetSeries`
        - :attr:`isPartOf` — links the dataset to a catalog or another broader dataset that this dataset belongs to

    **Example**
        >>> dataset = Dataset()
        >>> dataset.title = "Population Data 2024"
        >>> dataset.version = "1.0"
    """

    URL_PATH = "dataset"

    _WRITE_PROPERTIES = [
        "distribution",
        "inSeries",
        "temporal",
        "hasQualityMeasurement",
        "isPartOf",
        "title",
        "license",
        "theme",
        "version",
        "issued",
        "publisher",
        "creator",
    ]
    _READ_PROPERTIES = []
    _CLASS_PROPERTIES = _READ_PROPERTIES + _WRITE_PROPERTIES

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(fair_data_point, iri, uuid, *args, **kwargs)

        self._tainted = False

        self._rdf.bind("dqv", DQV)
        self._rdf.bind("ldqd", LDQD)

        self._rdf.add((self._iri, RDF.type, DCAT.Dataset))

    ###########################################################################
    # DCATv3 Class properties                                                 #
    ###########################################################################
    def add_distribution(
            self,
            distribution: Distribution | Graph | list[Distribution]) -> None:
        """
        Add one or more distributions to the Dataset.

        This function accepts either a single :class:`Distribution` instance an
        :class:`rdflib.graph.Graph` object containing distribution data, or a
        list of :class:`Distribution` instances.  The provided distribution(s)
        are added to the instance RDF graph, creating the corresponding RDF
        triples as needed.

        :param distribution: The distribution or distributions to add.
                       It can be one of the following:

                       - An :class:`Distribution` instance
                       - An :class:`rdflib.graph.Graph` instance
                       - A list of :class:`Distribution` instances
        :type distribution: Distribution | rdflib.Graph | list[Distribution]
        :return: None
        :rtype: None
        :raises TypeError: If the input type is not supported.

        .. note::
            - When a list is provided, each element must be an instance of
                :class:`Distribution`
            - When a :class:`rdflib.graph.Graph` is provided and it contains
                more than one distribution description, **all distributions**
                found in the graph are added.
        """
        if distribution is None:
            return

        _distribution_list = []

        if isinstance(distribution, Graph):
            for distribution_iri in distribution.objects(None,
                                                         DCAT.distribution):
                distribution_graph = distribution.cbd(distribution_iri)

                _d = Distribution()
                _d._content_setter(distribution_graph)

                _distribution_list.append(_d)
            raise NotImplementedError()
        elif isinstance(distribution, Distribution):
            _distribution_list.append(distribution)
        elif isinstance(distribution, list):
            for _d in distribution:
                _distribution_list.append(_d)
        else:
            raise TypeError((f"Type {type(distribution)} is not valid for "
                             "\"add_distribution()\" argument"))

        if self._distribution is None:
            self._distribution = dict()

        for _d in _distribution_list:
            self._distribution.update({_d.iri: _d})

            self._rdf.add((
                self._iri,
                DCAT.distribution,
                _d.iri
            ))

            self._rdf += _d.rdf

    @property
    def distribution(self) -> dict:
        """
        The ``dcat:distribution`` property.

        The setter for this property is the function ``add_distribution``.
        """
        return self._distribution

    @property
    def hasQualityMeasurement(self) -> dict:
        """
        The ``dcat:hasQualityMeasurement`` propery of the dataset.

        It provides the quality measurement associated with this resource.

        This property links the dataset to a specific quality measurement
        instance, such as completeness or accuracy.

        :param value: an instance of ``CompletenessMeasurement`` describing
            dataset quality.
        :type value: CompletenessMeasurement
        :rtype: CompletenessMeasurement
        :return: The ``CompletenessMeasurement`` instance representing the
            quality measurement.
        :raises TypeError: If the provided value is not a
            ``CompletenessMeasurement`` instance.
        """
        return self._hasQualityMeasurement

    @hasQualityMeasurement.setter
    def hasQualityMeasurement(self,
                              quality_measurement: CompletenessMeasurement):
        if isinstance(quality_measurement, CompletenessMeasurement):
            self._hasQualityMeasurement = quality_measurement
            self._rdf += self._hasQualityMeasurement.rdf

            self._tainted = True
        else:
            raise TypeError(
                (
                    "hasQualityMeasurement must be a "
                    "CompletenessMeasurement's  class instance."
                )
            )

        self._rdf.add(
            (
                self._iri,
                DCAT.hasQualityMeasurement,
                self._hasQualityMeasurement.iri,
            )
        )

        self._rdf.add(
            (self._hasQualityMeasurement.iri, DQV.computedOn, self._iri)
        )

    @property
    def inSeries(self) -> dict:
        """
        The ``dcat:inSeries`` property of the dataset.

        The link to the dataset series this resource belongs to.

        :type: :class:`str`, :class:`rdflib.term.URIRef`

        :rtype: :class:`str`
        :returns: The dataset's series.
        :returns: The dataset's ``isPartOf`` relationship.
        :raises TypeError: if the provided value is not a valid IRI, UUID, or
            NodeIdentifier.
        """
        return self._inSeries

    @inSeries.setter
    def inSeries(self, in_series: str or IdentifiedNode):
        if type(in_series) is str:
            self._inSeries = URIRef(in_series)

            self._tainted = True
        elif isinstance(in_series, IdentifiedNode):
            self._inSeries = in_series

            self._tainted = True
        else:
            raise TypeError(
                (
                    "inSeries must be a str or IdentifiedNode's "
                    "class instance (BNode or URIRef)"
                )
            )

        self._rdf.add((self._iri, DCAT.inSeries, self._inSeries))

    @property
    def isPartOf(self) -> dict:
        """
        The ``dcterms:isPartOf`` property of the dataset.

        The link to the parent resource, such as a dataset or catalog.

        :type: :class:`str`, :class:`rdflib.term.URIRef`

        :rtype: :class:`str`
        :returns: The dataset's ``isPartOf`` relationship.
        :raises TypeError: if the provided value is not a valid IRI, UUID, or
            NodeIdentifier.
        """
        return self._isPartOf

    @isPartOf.setter
    def isPartOf(self, is_part_of: str or IdentifiedNode):
        if type(is_part_of) is str:
            self._isPartOf = URIRef(is_part_of)

            self._tainted = True
        elif isinstance(is_part_of, IdentifiedNode):
            self._isPartOf = is_part_of

            self._tainted = True
        else:
            raise TypeError(
                (
                    "isPartOf must be a str or IdentifiedNode's "
                    "class instance (BNode or URIRef)"
                )
            )

        self._rdf.add((self._iri, DCTERMS.isPartOf, self._isPartOf))

    @property
    def temporal(self) -> dict:
        """
        The temporal coverage propery of the dataset.

        This property represents the time period during which the described
        dataset is collected.

        :param value: an instance of ``PeriodOfTime`` representing the time
            period of the resource.
        :type value: PeriodOfTime

        :return: the ``PeriodOfTime`` instance describing the temporal
            coverage.
        :rtype: PeriodOfTime
        :raises TypeError: if the provided value is not a ``PeriodOfTime``
            instance
        """
        return self._temporal

    @temporal.setter
    def temporal(self, temporal_coverage: PeriodOfTime):
        if isinstance(temporal_coverage, PeriodOfTime):
            self._temporal = temporal_coverage
            self._rdf += temporal_coverage.rdf

            self._tainted = True
        else:
            raise TypeError(
                ("temporal must be a PeriodOfTime's " "class instance")
            )

        self._rdf.add((self._iri, DCTERMS.temporal, self._temporal.iri))

    ###########################################################################

    # @property
    # def properties(self):
    #     """The DCATv3 Catalog class properties available.

    #     :returns: a list of the Catalog class properties available.
    #     :rtype: list of str
    #     """
    #     return self._PROPERTIES

    @property
    def rdf(self) -> str:
        return self._rdf

    def __str__(self):
        return (f"<Dataset uuid={self._uuid}, title=\"{self._title}\""
                ", {}>".format("tainted" if self._tainted else "not tainted"))


class DatasetSeries(Dataset):
    """Class representing a DCATv3 DatasetSerie.

    :var uuid: the uuid that is assigned by the Fair Data Point
    :vartype uuid: str
    """

    URL_PATH = "dataset-series"

    # _CLASS_PROPERTIES = []

    __frozen = False

    def __init__(
        self,
        fair_data_point: fdp.fairdatapoint.FairDataPoint = None,
        iri: str = None,
        uuid: str = None,
    ):
        super().__init__(fair_data_point, iri, uuid)

        self._tainted = False

        self._rdf.add((self._iri, RDF.type, DCAT.DatasetSeries))
