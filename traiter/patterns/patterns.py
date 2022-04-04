"""Common functions and data for all pattern types."""
from typing import Any

SpacyPatterns = list[list[dict[str, Any]]]
Decoder = dict[str, dict]
PatternArg = str | list[str] | SpacyPatterns
CompilerPatterns = list[str]
