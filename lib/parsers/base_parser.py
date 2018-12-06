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
        self.max = 0
        if self.rules:
            self.max = max(len(k.split()) for k, v in self.rules.items())

    @abstractmethod
    def get_rules(self):
        """List the parser rules here."""
        return {}

    def parse(self, input):
        """Parse the tokens."""
        tokens = self.lexer.tokenize(input)
        tokens.append(self.lexer.sentinel_token)

        stack = []
        results = []

        while tokens:
            count = min(len(stack), self.max)

            for idx in range(count, 0, -1):
                key = ' '.join([t['token'] for t in stack[-idx:]])
                match = self.rules.get(key)

                if self._find_lookahead(tokens, stack, key):
                    break

                if self._reduce(input, stack, results, match, idx):
                    break

            else:
                self._shift(tokens, stack)

        return results

    def value_span(self, stack, input, args):
        """Handle the case where the value spans one or more tokens."""
        span = args['span']
        print(args['span'])

        if len(span) == 1:
            value = stack[span[0]]['value']
        else:
            value = input[stack[span[0]]['start']:stack[span[1]]['end']]

        return {'value': value,
                'start': stack[0]['start'],
                'end': stack[-1]['end']}

    def _shift(self, tokens, stack, token=None):
        """Shift the next token onto the stack."""
        stack.append(tokens.pop(0))

    def _reduce(self, input, stack, results, match, idx):
        """Reduce the stack given the rule."""
        action = match['action'] if match else None

        if callable(action):
            results.append(action(stack[-idx:], input, match['args']))
            del stack[-idx:]
            return True
        elif action:
            token = {
                'token': action,
                'value': input[stack[-idx]['start']:stack[-1]['end']],
                'start': stack[-idx]['start'],
                'end': stack[-1]['end']}
            del stack[-idx:]
            stack.append(token)
            return True
        return False

    def _find_lookahead(self, tokens, stack, key):
        """Lookahead into the token list.

        We are looking for the longest lookahead that matches. If we find one
        we advance the stack to the lookahead.
        """
        for lookahead in self.lookahead.get(key, []):
            for i, token in enumerate(lookahead):
                if len(tokens) < i + 1 or tokens[i]['token'] != token:
                    break
            else:
                for _ in range(len(lookahead)):
                    self._shift(tokens, stack)
                return True
        return False

    def _build_rules(self):
        """Build the parser rules and check for simple errors."""
        self.rules = {' '.join(k.split()): v
                      for k, v in self.get_rules().items()}

    def _validate_rules(self):
        """Make sure rule tokens are found in the lexer."""
        valid_tokens = {t[0] for t in self.lexer.tokens}
        valid_tokens |= {v['action'] for k, v in self.rules.items()}

        errors = {}
        for rule, _ in self.rules.items():
            for token in rule.split():
                if token not in valid_tokens:
                    errors.add(token)

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
