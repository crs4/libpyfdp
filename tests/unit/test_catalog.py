# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest

from fdp.catalog import Catalog

from test_resource import TestResource


class TestCatalog(TestResource):
    """Test case for the Catalog class."""

    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return Catalog
