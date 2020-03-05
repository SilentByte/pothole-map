"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

from collections.abc import MutableMapping


class CaseInsensitiveDict(MutableMapping):
    def __init__(self, data=None, **kwargs):
        self._data = {}
        self.update({} if data is None else data, **kwargs)

    def __setitem__(self, key, value):
        self._data[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._data[key.lower()][1]

    def __delitem__(self, key):
        del self._data[key.lower()]

    def __iter__(self):
        return (k for k, _ in self._data.values())

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for k, v in self.items():
            if k not in other:
                return False

            if v != other[k]:
                return False

        return True

    def __repr__(self):
        return repr(dict(self.items()))
