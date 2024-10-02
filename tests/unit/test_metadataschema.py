# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
import uuid

import pytest

from fdp.metadataschema import MetadataSchema


class TestMetadataSchema:
    # version_tuple = (1, 0, 0)
    # version_string = '1.0.0'
    # license_url = 'https://creativecommons.org/publicdomain/zero/1.0/'
    # theme_url = 'https://inspire.ec.europa.eu/theme/pf'

    ###########################################################################
    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return MetadataSchema

    def test_set_unknown_property(self, testing_class):
        """Checks if an unknown property can be set."""

        meta_sch = testing_class()
        with pytest.raises(TypeError):
            meta_sch.unknown = True

    def test_get_properties(self, testing_class):
        """Checks if all the class's properties are readable."""

        meta_sch = testing_class()
        for _prop in meta_sch.properties:
            assert getattr(meta_sch, _prop) in [None, set(), {}]

    def test_set_name(self, testing_class):
        """Checks the Metadata Schema's name property setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.name is None
        assert meta_sch.tainted is False

        # Property set as a str
        meta_sch = testing_class()
        meta_sch.name = "A Metadata Schema"
        assert type(meta_sch.name) is str
        assert meta_sch.name == "A Metadata Schema"
        assert meta_sch.tainted is True

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.name = 15
        assert meta_sch.name is None
        assert meta_sch.tainted is False

    def test_set_description(self, testing_class):
        """Checks the Metadata Schema's description property setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.description is None
        assert meta_sch.tainted is False

        # Property set as a str
        meta_sch = testing_class()
        meta_sch.description = "A Metadata Schema Description"
        assert type(meta_sch.description) is str
        assert meta_sch.description == "A Metadata Schema Description"
        assert meta_sch.tainted is True

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.description = 15
        assert meta_sch.description is None
        assert meta_sch.tainted is False

    def test_set_definition(self, testing_class):
        """Checks the Metadata Schema's definition property setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.definition is None
        assert meta_sch.tainted is False

        # Property set as a str containing an RDF graph
        meta_sch = testing_class()
        meta_sch.definition = "@prefix: <http://fairdatapoint.org/> ."
        assert type(meta_sch.definition) is str
        assert meta_sch.definition == "@prefix: <http://fairdatapoint.org/> ."
        assert meta_sch.tainted is True

        # Property set as a str but not an RDF graph
        meta_sch = testing_class()
        with pytest.raises(ValueError):
            meta_sch.definition = "A Metadata Schema Description"
        assert meta_sch.definition is None
        assert meta_sch.tainted is False

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.definition = 15
        assert meta_sch.definition is None
        assert meta_sch.tainted is False

    def test_set_suggestedResourceName(self, testing_class):
        """Checks the Metadata Schema's suggestedResourceName property
        setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.suggestedResourceName is None
        assert meta_sch.tainted is False

        # Property set as a str
        meta_sch = testing_class()
        meta_sch.suggestedResourceName = "A Suggested Resource Name"
        assert type(meta_sch.suggestedResourceName) is str
        assert meta_sch.suggestedResourceName == "A Suggested Resource Name"
        assert meta_sch.tainted is True

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.suggestedResourceName = 15
        assert meta_sch.suggestedResourceName is None
        assert meta_sch.tainted is False

    def test_set_suggestedUrlPrefix(self, testing_class):
        """Checks the Metadata Schema's suggestedUrlPrefix property
        setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.suggestedUrlPrefix is None
        assert meta_sch.tainted is False

        # Property set as a str
        meta_sch = testing_class()
        meta_sch.suggestedUrlPrefix = "A Suggested URL Prefix"
        assert type(meta_sch.suggestedUrlPrefix) is str
        assert meta_sch.suggestedUrlPrefix == "A Suggested URL Prefix"
        assert meta_sch.tainted is True

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.suggestedUrlPrefix = 15
        assert meta_sch.suggestedUrlPrefix is None
        assert meta_sch.tainted is False

    def test_set_abstractSchema(self, testing_class):
        """Checks the Metadata Schema's abstractSchema property
        setter/getter."""

        # Property not set
        meta_sch = testing_class()
        assert meta_sch.abstractSchema is None
        assert meta_sch.tainted is False

        # Property set as a bool
        meta_sch = testing_class()
        meta_sch.abstractSchema = True
        assert type(meta_sch.abstractSchema) is bool
        assert meta_sch.abstractSchema is True
        assert meta_sch.tainted is True

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.abstractSchema = 15
        assert meta_sch.abstractSchema is None
        assert meta_sch.tainted is False

    def test_add_extends_schemas(self, testing_class):
        """Tests the extendsSchemaUuids property's setter/getter."""

        meta_sch = testing_class()
        assert meta_sch.extendsSchemaUuids is not None
        assert len(meta_sch.extendsSchemaUuids) == 0

        _uuid = str(uuid.uuid1())
        meta_sch.add_extendsSchemaUuids(_uuid)

        assert len(meta_sch.extendsSchemaUuids) == 1

        uuids = []
        uuids.append(_uuid)

        _uuid = str(uuid.uuid1())
        meta_sch.add_extendsSchemaUuids(_uuid)

        assert len(meta_sch.extendsSchemaUuids) == 2

        uuids.append(_uuid)

        # check duplications
        meta_sch.add_extendsSchemaUuids(_uuid)

        assert len(meta_sch.extendsSchemaUuids) == 2

        for _uuid in meta_sch.extendsSchemaUuids:
            assert _uuid in uuids

        meta_sch = testing_class()

        meta_schema_1 = MetadataSchema()
        meta_schema_2 = MetadataSchema()

        with pytest.raises(ValueError):
            meta_sch.add_extendsSchemaUuids(meta_schema_1)
        assert len(meta_sch.extendsSchemaUuids) == 0

        with pytest.raises(ValueError):
            meta_sch.add_extendsSchemaUuids(meta_schema_2)
        assert len(meta_sch.extendsSchemaUuids) == 0

        meta_sch = testing_class()

        meta_schema_1 = MetadataSchema(uuid=str(uuid.uuid1()))
        meta_schema_2 = MetadataSchema(uuid=str(uuid.uuid1()))

        meta_sch.add_extendsSchemaUuids(meta_schema_1)
        assert len(meta_sch.extendsSchemaUuids) == 1

        meta_sch.add_extendsSchemaUuids(meta_schema_2)
        assert len(meta_sch.extendsSchemaUuids) == 2

        # Property set as an incompatible data type
        meta_sch = testing_class()

        with pytest.raises(TypeError):
            meta_sch.add_extendsSchemaUuids(15)

        assert len(meta_sch.extendsSchemaUuids) == 0
        assert meta_sch.tainted is False
