"""Class to hold token regular expression data."""

from typing import Pattern, Callable
from dataclasses import dataclass


@dataclass
class Regexp:
    """Regular expression data."""

    type: str = None
    name: str = None
    token: str = None
    regexp: Pattern = None
    func: Callable = None
