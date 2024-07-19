# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
import uuid

import pytest

from fdp.metadataschema import MetadataSchema
from fdp.resourcedefinition import ResourceDefinition


class TestResourceDefinitions:
    # version_tuple = (1, 0, 0)
    # version_string = '1.0.0'
    # license_url = 'https://creativecommons.org/publicdomain/zero/1.0/'
    # theme_url = 'https://inspire.ec.europa.eu/theme/pf'

    ###########################################################################
    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return ResourceDefinition

    def test_set_unknown_property(self, testing_class):
        """Checks if an unknown property can be set."""

        res_def = testing_class()
        with pytest.raises(TypeError):
            res_def.unknown = True

    def test_set_name(self, testing_class):
        """Checks the Resource Definition's name property setter/getter."""

        # Property not set
        res_def = testing_class()
        assert res_def.name is None
        assert res_def.tainted is False

        # Property set as a str
        res_def = testing_class()
        res_def.name = "A Resource Definition"
        assert type(res_def.name) is str
        assert res_def.name == "A Resource Definition"
        assert res_def.tainted is True

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.name = 15
        assert res_def.name is None
        assert res_def.tainted is False

    def test_set_url_prefix(self, testing_class):
        """Checks the Resource Definition's url_prefix property setter/getter.
        """

        # Property not set
        res_def = testing_class()
        assert res_def.url_prefix is None
        assert res_def.tainted is False

        # Property set as a str
        res_def = testing_class()
        res_def.url_prefix = "new_resource"
        assert type(res_def.url_prefix) is str
        assert res_def.url_prefix == "new_resource"
        assert res_def.tainted is True

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.url_prefix = 15
        assert res_def.url_prefix is None
        assert res_def.tainted is False

    def test_add_metadata_schemas(self, testing_class):
        """Tests the metadata_schemas property's setter/getter."""

        res_def = testing_class()
        assert res_def.metadata_schemas is not None
        assert len(res_def.metadata_schemas) == 0

        _uuid = str(uuid.uuid1())
        res_def.add_metadata_schema(_uuid)

        assert len(res_def.metadata_schemas) == 1

        uuids = []
        uuids.append(_uuid)

        _uuid = str(uuid.uuid1())
        res_def.add_metadata_schema(_uuid)

        assert len(res_def.metadata_schemas) == 2

        uuids.append(_uuid)

        # check duplications
        res_def.add_metadata_schema(_uuid)

        assert len(res_def.metadata_schemas) == 2

        for _uuid in res_def.metadata_schemas:
            assert _uuid in uuids

        res_def = testing_class()

        meta_schema_1 = MetadataSchema()
        meta_schema_2 = MetadataSchema()

        with pytest.raises(ValueError):
            res_def.add_metadata_schema(meta_schema_1)
        assert len(res_def.metadata_schemas) == 0

        with pytest.raises(ValueError):
            res_def.add_metadata_schema(meta_schema_2)
        assert len(res_def.metadata_schemas) == 0

        res_def = testing_class()

        meta_schema_1 = MetadataSchema(uuid=str(uuid.uuid1()))
        meta_schema_2 = MetadataSchema(uuid=str(uuid.uuid1()))

        res_def.add_metadata_schema(meta_schema_1)
        assert len(res_def.metadata_schemas) == 1

        res_def.add_metadata_schema(meta_schema_2)
        assert len(res_def.metadata_schemas) == 2

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.add_metadata_schema(15)

        assert len(res_def.metadata_schemas) == 0
        assert res_def.tainted is False

    def test_add_child(self, testing_class):
        """Tests the children property's setter/getter."""

        res_def = testing_class()
        assert res_def.children is not None
        assert len(res_def.children) == 0

        uuids = []

        # Tests for the relation_uri argument presence
        _uuid = str(uuid.uuid1())
        with pytest.raises(TypeError):
            res_def.add_child(_uuid)

        assert len(res_def.children) == 0

        res_def.add_child(_uuid, 'http://www.w3.org/ns/dcat#dataset')
        assert len(res_def.children) == 1

        uuids.append(_uuid)

        _uuid = str(uuid.uuid1())
        res_def.add_child(_uuid, 'http://www.w3.org/ns/dcat#catalog')
        assert len(res_def.children) == 2

        uuids.append(_uuid)

        # check duplications
        res_def.add_child(_uuid, 'http://www.w3.org/ns/dcat#catalog')

        assert len(res_def.children) == 2

        for _uuid in res_def.children:
            assert _uuid in uuids

        res_def = testing_class()

        child_1 = ResourceDefinition()
        child_2 = ResourceDefinition()

        with pytest.raises(ValueError):
            res_def.add_child(child_1, 'http://www.w3.org/ns/dcat#catalog')
        assert len(res_def.children) == 0

        with pytest.raises(ValueError):
            res_def.add_child(child_2, 'http://www.w3.org/ns/dcat#catalog')
        assert len(res_def.children) == 0

        res_def = testing_class()

        child_1 = ResourceDefinition(uuid=str(uuid.uuid1()))
        child_2 = ResourceDefinition(uuid=str(uuid.uuid1()))

        res_def.add_child(child_1, 'http://www.w3.org/ns/dcat#catalog')
        assert len(res_def.children) == 1

        res_def.add_child(child_2, 'http://www.w3.org/ns/dcat#catalog')
        assert len(res_def.children) == 2

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.add_child(15, 'http://www.w3.org/ns/dcat#catalog')

        assert len(res_def.children) == 0
        assert res_def.tainted is False
