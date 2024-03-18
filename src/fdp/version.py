class Version(object):
    def __init__(self, version: str = None, major: int = None,
                 minor: int = None, patch: int = None):
        if version:
            _major, _minor, _patch = version.split('.')
            self._major = int(_major)
            self._minor = int(_minor)
            self._patch = int(_patch)
        else:
            self._major = major
            self._minor = minor
            self._patch = patch

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, major: int):
        self._major = major

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, minor: int):
        self._minor = minor

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, patch: int):
        self._patch = patch
        return self

    def reset(self):
        self._major = 1
        self._minor = 0
        self._patch = 0
        return self

    def as_str(self):
        _l = [self._major, self._minor, self._patch]

        if any(_l):
            return '.'.join(map(str, _l))

        return None

    def __str__(self):
        return (f"<Version: {self.as_str()}, major: {self._major}, "
                f"minor: {self._minor}, patch: {self._patch}>")

    def __repr__(self):
        return self.__str__()
