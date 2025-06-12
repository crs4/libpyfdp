# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=unidiomatic-typecheck,too-many-instance-attributes
import json

import fdp


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, fdp.version.Version):
            return obj.as_str()
        return json.JSONEncoder.default(self, obj)


class LibFDPError(RuntimeError):
    """Class for general LibFDP Errors."""
    def __init__(self, message):
        super().__init__(message)


class AlreadyPresentError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class NotPresentError(RuntimeError):
    def __init__(self, message=""):
        super().__init__(message)


class InstanceOverrideError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class IncompatibleClassError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
