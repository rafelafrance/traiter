"""Common functions and data for all pattern types."""
from typing import Any
from typing import Union

SpacyPatterns = list[list[dict[str, Any]]]
Decoder = dict[str, dict]
PatternArg = Union[str, list[str], SpacyPatterns]
CompilerPatterns = list[str]
