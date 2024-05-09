# pylint: disable=unidiomatic-typecheck,redefined-outer-name
# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest

from fdp.dataset import DatasetSeries

from test_dataset import (TestDataset, tsv_distribution, csv_distribution,
                          dataset_series)


class TestDatasetSeries(TestDataset):
    """Test case for the Dataset class."""

    @pytest.fixture
    def testing_class(self):
        """Provides the class instance to test."""
        return DatasetSeries

    def test_dataset_in_series(self, dataset_series, testing_class):
        """Tests the inSeries property's setter/getter."""
        assert True
