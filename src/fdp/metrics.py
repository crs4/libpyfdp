# pylint: disable=unidiomatic-typecheck,invalid-name,missing-module-docstring
# pylint: disable=too-many-instance-attributes

from rdflib import URIRef, Literal, Graph, BNode
from rdflib.namespace import DCTERMS, DCAT, XSD, RDF, Namespace, SKOS

import fdp.fairdatapoint

DQV = Namespace("http://www.w3.org/ns/dqv#")


class PointDensityDimension():
    """Class representing the point density dimension in timeseries."""

    # _POINTDENSITYMETRIC_PROPERTIES = ['algorithm', 'checksumValue']

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        # for _p in self._POINTDENSITYMETRIC_PROPERTIES:
        #     setattr(PointDensityMetric, f'_{_p}', None)

        self._rdf = Graph()
        self._rdf.bind("dqv", DQV)
        self._rdf.bind("skos", SKOS)

        self._uuid = uuid

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
            # self._iri = BNode()
            self._iri = URIRef("cadiglab:dataDensityDimension")

        self._tainted = False

        self.__frozen = True

        self._rdf.add((
            self._iri,
            RDF.type,
            DQV.Dimension))

        self._rdf.add((
            self._iri,
            SKOS.prefLabel,
            Literal("Completeness", lang='en')))

        self._rdf.add((
            self._iri,
            SKOS.definition,
            Literal("Completeness refers to the degree to "
                    "which all required information is "
                    "present in a particular dataset.",
                    lang='en')))

        #  _iso_inherent_data_quality = BNode()
        _iso_inherent_data_quality = URIRef("iso:inherentDataQuality")

        self._rdf.add((
            _iso_inherent_data_quality,
            RDF.type,
            DQV.Category))

        self._rdf.add((
            _iso_inherent_data_quality,
            SKOS.prefLabel,
            Literal("Inherent Data Quality", lang='en')))

        self._rdf.add((
            self._iri,
            DQV.inCategory,
            _iso_inherent_data_quality))

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the PointDensityDimension instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the PointDensityDimension instance."""
        return self._rdf


class PointDensityMetric():
    """Class representing the point density metric in timeseries."""

    # _POINTDENSITYMETRIC_PROPERTIES = ['algorithm', 'checksumValue']

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        # for _p in self._POINTDENSITYMETRIC_PROPERTIES:
        #     setattr(PointDensityMetric, f'_{_p}', None)

        self._rdf = Graph()
        self._rdf.bind("dqv", DQV)
        self._rdf.bind("skos", SKOS)

        self._uuid = uuid

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
            # self._iri = BNode()
            self._iri = URIRef("cadiglab:dataDensityMetric")

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
        point_density_dimension = PointDensityDimension()

        self._rdf.add((
            self._iri,
            DQV.inDimension,
            point_density_dimension.iri))

        self._rdf += point_density_dimension.rdf

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(f"Property '{key}' is not valid.")
        super().__setattr__(key, value)

    @property
    def iri(self):
        """The iri of the PointDensityMetric instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the PointDensityMetric instance."""
        return self._rdf


class DQVMeasurement():
    """Class representing a DQV Measurement."""

    _DQVMEASUREMENT_PROPERTIES = ['isMeasurementOf', 'value']

    __frozen = False

    def __init__(self, iri: str = None, uuid: str = None):
        for _p in self._DQVMEASUREMENT_PROPERTIES:
            setattr(DQVMeasurement, f'_{_p}', None)

        self._rdf = Graph()
        self._rdf.bind("dqv", DQV)

        self._uuid = uuid

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
            # self._iri = BNode()
            self._iri = URIRef("cadiglab:densityMeasurement")

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
        """The iri of the DQVMeasurement instance."""
        return self._iri

    @property
    def rdf(self):
        """The rdf graph of the DQVMeasurement instance."""
        return self._rdf

    @property
    def isMeasurementOf(self) -> dict:
        """The associated metric to the DQV Measurement."""
        return self._isMeasurementOf

    @isMeasurementOf.setter
    def isMeasurementOf(self, metric: PointDensityMetric):
        if isinstance(metric, PointDensityMetric):
            self._isMeasurementOf = metric
            self._rdf += self._isMeasurementOf.rdf

            self._tainted = True
        else:
            raise TypeError(("isMeasurementOf must be a PointDensityMetric's "
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
