import pytest
# from rdflib import Literal, URIRef, BNode
# import uuid

from fdp.version import Version


class TestVersion:
    version_tuple = (1, 0, 0)
    version_string = '1.0.0'

    ###########################################################################
    def test_version_init_default(self):
        """Checks the Version's initializer."""

        # Property not set
        version = Version()
        assert type(version) is Version
        assert version == Version('1.0.0')

    def test_version_init_as_str(self):
        """Checks the Version's initializer."""

        # Property set as a str
        version = Version(self.version_string)
        assert type(version) is Version
        assert version == Version(self.version_tuple)

    def test_version_init_as_tuple(self):
        """Checks the Version's initializer."""

        # Property set as a Tuple
        version = Version(self.version_tuple)
        assert type(version) is Version
        assert version == Version(self.version_string)

    def test_version_init_as_incomplete_tuple(self):
        """Checks the Version's initializer."""

        # Property set as an incomplete Tuple
        version = Version((1,))
        assert type(version) is Version
        assert version == Version('1.0.0')

        version = Version((1, 0, ))
        assert type(version) is Version
        assert version == Version('1.0.0')

        version = Version((0, 1, ))
        assert type(version) is Version
        assert version == Version('0.1.0')

        version = Version((0, 0, 1))
        assert type(version) is Version
        assert version == Version('0.0.1')

    def test_version_init_as_incomplete_str(self):
        """Checks the Version's initializer."""

        # Property set as a str
        version = Version('1')
        assert type(version) is Version
        assert version == Version((1, 0, 0))

        version = Version('1.2')
        assert type(version) is Version
        assert version == Version((1, 2, 0))

        version = Version('1.2.3')
        assert type(version) is Version
        assert version == Version((1, 2, 3))

        version = Version('0')
        assert type(version) is Version
        assert version == Version((0, 0, 0))

        version = Version('0.1')
        assert type(version) is Version
        assert version == Version((0, 1, 0))

        version = Version('0.0.3')
        assert type(version) is Version
        assert version == Version((0, 0, 3))

    def test_version_init_as_wrong_str(self):
        """Checks the Version's initializer."""

        with pytest.raises(ValueError):
            Version('a.b.c')

        with pytest.raises(ValueError):
            Version('1.b.c')

        with pytest.raises(ValueError):
            Version('1.2.')

        with pytest.raises(ValueError):
            Version('.2.3')

    def test_version_init_as_wrong_tuple(self):
        """Checks the Version's initializer."""

        with pytest.raises(ValueError):
            Version(('a', 2, 3))

        with pytest.raises(ValueError):
            Version((1, 'a', 2))

        with pytest.raises(ValueError):
            Version((1, 2, 'a'))

    def test_version_setter_getter(self):
        """Checks the Version's setter/getter."""

        # Property set as a str
        version = Version()
        assert type(version) is Version
        assert version == Version((1, 0, 0))

        version.major = 10
        assert version == Version((10, 0, 0))

        version.minor = 20
        assert version == Version((10, 20, 0))

        version.patch = 30
        assert version == Version((10, 20, 30))

    def test_version_reset(self):
        """Checks the Version's reset."""

        # Property set as a str
        version = Version('1.2.3')
        assert type(version) is Version
        assert version == Version((1, 2, 3))

        version.reset()
        assert type(version) is Version
        assert version == Version((1, 0, 0))
