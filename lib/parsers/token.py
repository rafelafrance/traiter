"""Class to hold token data."""

from typing import Dict
from dataclasses import dataclass, field as datafield


@dataclass
class Token:
    """Token data."""

    token: str = None
    name: str = None
    groups: Dict = datafield(default_factory={})
    start: int = 0
    end: int = 0
