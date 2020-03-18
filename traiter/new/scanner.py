"""Scan an input string and create tokens."""

from typing import List, Optional, Pattern
import regex  # type: ignore
from .token import Token


class Scanner:
    """Scan text and create tokens."""

    def __init__(self):
        """Create a scanner."""
        self.clauses: List[str] = []
        self.compiled: bool = False
        self.regex: Optional[Pattern] = None

    def add(self, name: str, regexp: str):
        """Add a tokenizer rule."""
        self.clauses.append(f'(?<{name}>{regexp})')
        self.compiled = False

    def compile(self, flags=regex.IGNORECASE | regex.VERBOSE):
        """Compile the regex fragment strings into one regex."""
        self.compiled = True
        joined = '|'.join(self.clauses)
        self.regex = regex.compile(joined, flags=flags)

    def scan(self, text: str) -> List[Token]:
        """Break a string into tokens."""
        if not self.compiled:
            self.compile()

        return [
            Token(m.group(), genus=m.lastgroup, start=m.start(), end=m.end())
            for m in self.regex.finditer(text)]
