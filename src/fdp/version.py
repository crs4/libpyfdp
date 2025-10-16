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

class Version(object):
    def __init__(self, version: str or tuple(int, int, int) = None,
                 major: int = None, minor: int = None, patch: int = None):

        self._major = 1
        self._minor = 0
        self._patch = 0

        if version is not None:
            if type(version) is str:
                _version = version.split('.')

                self._major = (int(_version[0]) if len(_version) > 0 else
                               self._major)
                self._minor = (int(_version[1]) if len(_version) > 1 else
                               self._minor)
                self._patch = (int(_version[2]) if len(_version) > 2 else
                               self._patch)

            elif type(version) is tuple:
                self._major = (int(version[0]) if len(version) > 0 else
                               self._major)
                self._minor = (int(version[1]) if len(version) > 1 else
                               self._minor)
                self._patch = (int(version[2]) if len(version) > 2 else
                               self._patch)
        else:
            self._major = major or self._major
            self._minor = minor or self._minor
            self._patch = patch or self._patch

    def __eq__(self, other):
        return (self._major == other._major and
                self._minor == other._minor and
                self._patch == other._patch)

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

    def inc_major(self):
        """Increase the major number."""
        self._major = self._major + 1
        return self

    def inc_minor(self):
        """Increase the minor number."""
        self._minor = self._minor + 1
        return self

    def inc_patch(self):
        """Increase the patch number."""
        self._patch = self._patch + 1
        return self

    def __str__(self):
        return self.as_str()

    def __repr__(self):
        return (f"<Version: {self.as_str()}, major: {self._major}, "
                f"minor: {self._minor}, patch: {self._patch}>")
