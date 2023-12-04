from typing import Callable


class Template:
    def __init__(self):
        self._actions = []

    @property
    def reconcile(self) -> list[Callable]:
        return self._actions

    @reconcile.setter
    def reconcile(self, actions: list[Callable]):
        self._actions += actions


TEMPLATE = Template()


class Base:
    def __init__(self, *args):
        TEMPLATE.reconcile = args

    @staticmethod
    def search(other, keys: list[str], default=None):
        for key in keys:
            if other.get(key):
                return other[key]
        return default

    @staticmethod
    def wildcard(other, pattern: str, default=None):
        pattern = pattern.casefold()
        for key in other.keys():
            folded = key.casefold()
            if folded.find(pattern) > -1:
                return other[key]
        return default

    @staticmethod
    def case(*args) -> list[str]:
        keys = " ".join(args).split()
        keys += [k.lower() for k in keys]
        return sorted(set(keys))
