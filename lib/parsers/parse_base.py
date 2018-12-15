"""Parse the notations."""

from abc import abstractmethod
from lib.lexers.lex_base import Token


class ParseBase:
    """Shared parser logic."""

    def __init__(self, lexer):
        """Initialize the parser."""
        self.lexer = lexer()
        self.stack = []
        self.tokens = []
        self.rules = self.build_rules()
        self.validate_rules()
        self.windows = self.build_windows()

    @abstractmethod
    def rule_dict(self):
        """Return the parser rules for the trait.

        The key is the rule and the value is a dictionary containing:
            - An 'action' which can be either:
                - A string that will replace the entire rule.
                - A function for building the results. The rule is removed.
            - And an optional 'args' dictionary. This dictionary will be passed
              to the 'action' function above.
        """
        return {}

    def parse(self, raw):
        """Parse the tokens."""
        self.tokens = self.lexer.tokenize(raw)
        self.tokens.append(self.lexer.sentinel_token)

        self.stack = []
        results = []

        while self.tokens:

            rule, prod = self.find_longest_match()

            if rule:
                self.reduce(raw, results, prod)
            else:
                self.shift()

        return results

    def find_longest_match(self):
        """Look for the longest possible match using the top of the stack."""
        if not self.stack:
            return None, None

        tos = self.stack[-1].token
        windows = self.windows.get(tos, [])

        for look_back, look_ahead in windows:
            tokens = self.stack[-look_back:] + self.tokens[:look_ahead]
            rule = ' '.join(t.token for t in tokens)
            prod = self.rules.get(rule)

            if prod:
                for _ in range(look_ahead):
                    self.shift()
                return rule, prod

        return None, None

    def shift(self):
        """Shift the next token onto the stack."""
        self.stack.append(self.tokens.pop(0))

    def reduce(self, raw, results, prod):
        """Reduce the stack given the rule."""
        action = prod['action']
        rule_len = prod['len']
        if callable(action):
            result = action(self.stack[-rule_len:], raw, prod['args'])
            del self.stack[-rule_len:]
            results.append(result)
        elif action:
            token = Token(
                action, self.stack[-rule_len].start, self.stack[-1].end)
            del self.stack[-rule_len:]
            self.stack.append(token)

    def build_rules(self):
        """Build the parser rules and check for simple errors."""
        rules = {' '.join(k.split()): v
                 for k, v in self.rule_dict().items()}

        for rule, prod in rules.items():
            prod['len'] = rule.count(' ') + 1

        return rules

    def validate_rules(self):
        """Make sure rule tokens are found in the lexer."""
        if not self.rules:
            raise ValueError('No rules for the parser.')

        valid_tokens = {t.token for t in self.lexer.tokens}
        valid_tokens |= {v['action'] for k, v in self.rules.items()}

        errors = set()
        for rule, _ in self.rules.items():
            for token in rule.split():
                if token not in valid_tokens:
                    errors.add(f'"{token}"')

        if errors:
            raise ValueError(f'Unknown tokens: {", ".join(errors)}.')

    def build_windows(self):
        """How far to look into the stack and tokens for each token."""
        token_set = {t for k, v in self.rules.items() for t in k.split()}
        windows = {t: set() for t in token_set}

        for rule, prod in self.rules.items():
            tokens = rule.split()
            for i, token in enumerate(tokens):
                behind = i + 1
                ahead = prod['len'] - i - 1
                window = (behind, ahead)
                windows[token].add(window)

        # Sort so that longest window is first. Use look-behind as tiebreaker
        for token, window in windows.items():
            windows[token] = sorted(
                windows[token],
                key=lambda x: (x[0] + x[1], x[0]),
                reverse=True)

        return windows

    # pylint: disable=unused-argument, no-self-use
    def post_process(self, results, args=None):
        """Post-process the results."""
        return results
