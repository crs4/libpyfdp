# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
import json
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

    def test_set_urlPrefix(self, testing_class):
        """Checks the Resource Definition's urlPrefix property setter/getter.
        """

        # Property not set
        res_def = testing_class()
        assert res_def.urlPrefix is None
        assert res_def.tainted is False

        # Property set as a str
        res_def = testing_class()
        res_def.urlPrefix = "new_resource"
        assert type(res_def.urlPrefix) is str
        assert res_def.urlPrefix == "new_resource"
        assert res_def.tainted is True

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.urlPrefix = 15
        assert res_def.urlPrefix is None
        assert res_def.tainted is False

    def test_add_metadataSchemaUuids(self, testing_class):
        """Tests the metadataSchemaUuids property's setter/getter."""

        res_def = testing_class()
        assert res_def.metadataSchemaUuids is not None
        assert len(res_def.metadataSchemaUuids) == 0

        _uuid = str(uuid.uuid1())
        res_def.add_metadataSchemaUuids(_uuid)

        assert len(res_def.metadataSchemaUuids) == 1

        uuids = []
        uuids.append(_uuid)

        _uuid = str(uuid.uuid1())
        res_def.add_metadataSchemaUuids(_uuid)

        assert len(res_def.metadataSchemaUuids) == 2

        uuids.append(_uuid)

        # check duplications
        res_def.add_metadataSchemaUuids(_uuid)

        assert len(res_def.metadataSchemaUuids) == 2

        for _uuid in res_def.metadataSchemaUuids:
            assert _uuid in uuids

        res_def = testing_class()

        meta_schema_1 = MetadataSchema()
        meta_schema_2 = MetadataSchema()

        with pytest.raises(ValueError):
            res_def.add_metadataSchemaUuids(meta_schema_1)
        assert len(res_def.metadataSchemaUuids) == 0

        with pytest.raises(ValueError):
            res_def.add_metadataSchemaUuids(meta_schema_2)
        assert len(res_def.metadataSchemaUuids) == 0

        res_def = testing_class()

        meta_schema_1 = MetadataSchema(uuid=str(uuid.uuid1()))
        meta_schema_2 = MetadataSchema(uuid=str(uuid.uuid1()))

        res_def.add_metadataSchemaUuids(meta_schema_1)
        assert len(res_def.metadataSchemaUuids) == 1

        res_def.add_metadataSchemaUuids(meta_schema_2)
        assert len(res_def.metadataSchemaUuids) == 2

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(TypeError):
            res_def.add_metadataSchemaUuids(15)

        assert len(res_def.metadataSchemaUuids) == 0
        assert res_def.tainted is False

    def test_add_children(self, testing_class):
        """Tests the children property's setter/getter."""

        res_def = testing_class()
        assert res_def.children is not None
        assert len(res_def.children) == 0

        uuids = []

        # Tests for the relation_uri argument presence
        _uuid = str(uuid.uuid1())
        with pytest.raises(TypeError):
            res_def.add_children(_uuid)

        assert len(res_def.children) == 0

        res_def.add_children(
            {
                'resourceDefinitionUuid': _uuid,
                'relationUri': 'http://www.w3.org/ns/dcat#dataset',
                'listView': {
                    'title': 'Datasets',
                    'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                }
            })
        assert len(res_def.children) == 1

        uuids.append(_uuid)

        _uuid = str(uuid.uuid1())
        res_def.add_children(
            {
                'resourceDefinitionUuid': _uuid,
                'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                'listView': {
                    'title': 'Datasets',
                    'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                }
            })
        assert len(res_def.children) == 2

        uuids.append(_uuid)

        # check duplications
        res_def.add_children(
            {
                'resourceDefinitionUuid': _uuid,
                'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                'listView': {
                    'title': 'Datasets',
                    'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                }
            })

        assert len(res_def.children) == 3

        for _child in res_def.children:
            assert _child['resourceDefinitionUuid'] in uuids

        res_def = testing_class()

        child_1 = ResourceDefinition()
        child_2 = ResourceDefinition()

        with pytest.raises(TypeError):
            res_def.add_children(
                {
                    'resourceDefinitionUuid': child_1.uuid,
                    'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                    'listView': {
                        'title': 'Datasets',
                        'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                    }

                })
        assert len(res_def.children) == 0

        with pytest.raises(TypeError):
            res_def.add_children(
                {
                    'resourceDefinitionUuid': child_2.uuid,
                    'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                    'listView': {
                        'title': 'Datasets',
                        'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                    }

                })
        assert len(res_def.children) == 0

        res_def = testing_class()

        child_1 = ResourceDefinition(uuid=str(uuid.uuid1()))
        child_2 = ResourceDefinition(uuid=str(uuid.uuid1()))

        res_def.add_children(
            {
                'resourceDefinitionUuid': child_2.uuid,
                'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                'listView': {
                    'title': 'Datasets',
                    'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                }

            })
        assert len(res_def.children) == 1

        res_def.add_children(
            {
                'resourceDefinitionUuid': child_2.uuid,
                'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                'listView': {
                    'title': 'Datasets',
                    'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                }

            })
        assert len(res_def.children) == 2

        # Property set as an incompatible data type
        res_def = testing_class()

        with pytest.raises(KeyError):
            res_def.add_children(
                {
                    'attribute_1': child_2.uuid,
                    'relationUri': 'http://www.w3.org/ns/dcat#catalog',
                    'listView': {
                        'title': 'Datasets',
                        'tagsUri': 'http://www.w3.org/ns/dcat#theme'
                    }

                })

        assert len(res_def.children) == 0
        assert res_def.tainted is False

    def test_add_externalLinks(self, testing_class):
        """Tests the externalLinks property's setter/getter."""

        res_def = testing_class()
        assert res_def.externalLinks is not None
        assert len(res_def.externalLinks) == 0

        # uuids = []

        # Tests for the propertyUri argument presence
        with pytest.raises(KeyError):
            res_def.add_externalLinks(
                {
                    'title': 'A title',
                })

        # Tests for the title argument presence
        with pytest.raises(KeyError):
            res_def.add_externalLinks(
                {
                    'propertyUri': 'A property uri',
                })

        assert len(res_def.externalLinks) == 0

        res_def.add_externalLinks(
            {
                'title': 'A title',
                'propertyUri': 'A property uri',
            })

        assert len(res_def.externalLinks) == 1

        res_def.add_externalLinks(
            {
                'title': 'Another title',
                'propertyUri': 'Another property uri',
            })

        assert len(res_def.externalLinks) == 2

        # check duplications
        res_def.add_externalLinks(
            {
                'title': 'Another title',
                'propertyUri': 'Another property uri',
            })

        assert len(res_def.externalLinks) == 3

        for _link in res_def.externalLinks:
            assert _link['title'] in ['A title', 'Another title']

    def test__content(self, testing_class):
        """Tests the _content function."""
        res_def = testing_class()

        res_def.name = "A Resource Definition"
        _uuid = str(uuid.uuid1())
        res_def._uuid = _uuid

        _content = res_def._content()

        for k, v in json.loads(_content).items():
            if k == 'name':
                assert v == "A Resource Definition"
            if k == 'uuid':
                assert v == _uuid
