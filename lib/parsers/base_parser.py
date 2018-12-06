"""Parse the notations."""

from abc import abstractmethod


class BaseParser:
    """Shared parser logic."""

    def __init__(self, lexer):
        """Initialize the parser."""
        self.lexer = lexer()
        self.rules = {}
        self.lookahead = {}
        self._build_rules()
        self._validate_rules()
        self._build_lookahead()
        self.max = max(len(k.split()) for k, v in self.rules.items())

    @abstractmethod
    def get_rules(self):
        """List the parser rules here."""

    def parse(self, input):
        """Parse the tokens."""
        tokens = self.lexer.tokenize(input)
        tokens.append(self.lexer.sentinel_token)

        stack = []
        results = []

        while tokens:
            if not stack:
                stack.append(tokens.pop(0))
                continue

            count = min(len(stack), self.max)

            for j in range(count, 0, -1):
                key = ' '.join([t['token'] for t in stack[-j:]])
                production = self.rules.get(key)

                if self.find_lookahead(tokens, stack, key):
                    break

                if callable(production):
                    results.append(production(stack[-j:], input))
                    del stack[-j:]
                    break
                elif production:
                    token = {
                        'token': production,
                        'value': input[stack[-j]['start']:stack[-1]['end']],
                        'start': stack[-j]['start'],
                        'end': stack[-1]['end']}
                    del stack[-j:]
                    stack.append(token)
                    break
            else:
                stack.append(tokens.pop(0))

        return results

    def find_lookahead(self, tokens, stack, key):
        """
        Lookahead into the token list.

        We are looking longest lookahead to shortest lookahead. If we find one
        we advance the stack to the lookahead.
        """
        for lookahead in self.lookahead.get(key, []):
            for i, token in enumerate(lookahead):
                if len(tokens) < i + 1 or tokens[i]['token'] != token:
                    break
            else:
                for _ in range(len(lookahead)):
                    stack.append(tokens.pop(0))
                return True
        return False

    def range(self, stack, input):
        """Parse a number raange like 10 to 20 mm."""
        return

    def _build_rules(self):
        """Build the parser rules and check for simple errors."""
        self.rules = {' '.join(k.split()): v
                      for k, v in self.get_rules().items()}

    def _validate_rules(self):
        """Make sure rule tokens are found in the lexer."""
        valid_tokens = [t[0] for t in self.lexer.tokens]
        valid_tokens += [v for k, v in self.rules.items()
                         if isinstance(v, str)]

        errors = []
        for rule, _ in self.rules.items():
            tokens = rule.split()
            for token in tokens:
                if token not in valid_tokens:
                    errors.append(token)

        if errors:
            raise ValueError(f'Unknown tokens: {", ".join(errors)}.')

    def _build_lookahead(self):
        """Build the lookahead information for each token."""
        other_rules = [k for k, _ in self.rules.items()]
        for rule, _ in self.rules.items():
            self.lookahead[rule] = []
            for other_rule in other_rules:
                if other_rule.startswith(rule) and rule != other_rule:
                    lookahead = other_rule.replace(rule, '', 1).split()
                    self.lookahead[rule].append(lookahead)

        for rule, lookahead in self.lookahead.items():
            self.lookahead[rule] = sorted(lookahead, key=len, reverse=True)
