"""Build parser results."""

from typing import Any, List
from dataclasses import dataclass, field as datafield


@dataclass
class Result:
    """This is a rule production."""

    value: Any = None
    units: str = None
    trait: str = None
    field: str = None
    start: int = 0
    end: int = 0
    flags: dict = datafield(default_factory=dict)


Results = List[Result]
