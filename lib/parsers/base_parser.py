"""Parse the notations."""

from abc import abstractmethod


class BaseParser:
    """Shared parser logic."""

    @staticmethod
    def value_span(stack, raw, args):
        """Handle the case where the value spans one or more tokens."""
        span = args['span']

        if len(span) == 1:
            value = stack[span[0]]['value']
        else:
            value = raw[stack[span[0]]['start']:stack[span[1]]['end']]

        return {'value': value,
                'start': stack[0]['start'],
                'end': stack[-1]['end']}

    def __init__(self, lexer):
        """Initialize the parser."""
        self.lexer = lexer()
        self.too_many = 999999
        self.stack = []
        self.tokens = []
        self.rules = self.build_rules()
        self.validate_rules()
        # The maximum number of tokens in the rule set
        self.max_tokens = max(k.count(' ') for k, v in self.rules.items()) + 1

    @abstractmethod
    def rule_dict(self):
        """Return the parser rules for the trait.

        The key is the rule and the value is a dictonary containing:
            - An 'action' which can be either:
                - A string that will replace the entire rule.
                - A function reference that performs an action for the
                  reduction. This function will get the folling arguments:
                  - The portion of the stack that maches the the rule. So if
                    the stack is 10 tokens deep and the rule has 3 tokens in it
                    you will get the last (top) 3 items of the stack.
                  - The raw input string so we can get data from that.
                  - An arguments dictionary (see below).
            - And an optional 'args' dictionary. This dictionary will be passed
              to the 'action' function above.

            ** NOTE: The key is normalized and data may be added to the value.
        """
        return {}

    def parse(self, raw):
        """Parse the tokens."""
        self.tokens = self.lexer.tokenize(raw)
        self.tokens.append(self.lexer.sentinel_token)

        self.stack = []
        results = []

        while self.tokens:
            rule, prod = self.find_stack_match()

            if rule:
                rule, prod = self.find_longer_match(rule, prod)

                self.reduce(raw, results, prod)
            else:
                self.shift()

        return results if len(results) < self.too_many else []

    def find_stack_match(self):
        """Look for the longest possible rule at the top of the stack."""
        count = min(len(self.stack), self.max_tokens)
        for idx in range(count, 0, -1):
            rule = ' '.join([t['token'] for t in self.stack[-idx:]])
            prod = self.rules.get(rule)
            if prod:
                return rule, prod
        return None, None

    def find_longer_match(self, rule, prod):
        """Look ahead into the token list to find the longest possible match.

        I.e. we are looking for the longest rule that has the current rule as a
        prefix made up of the current rule and the next K tokens. If found, we
        advance the stack and return it.
        """
        count = min(len(self.tokens), self.max_tokens - prod['len'])
        for idx in range(count, 0, -1):
            longer_rule = \
                f"{rule} {' '.join([t['token'] for t in self.tokens[:idx]])}"
            longer_prod = self.rules.get(longer_rule)

            if longer_prod:
                for _ in range(idx):
                    self.shift()
                return longer_rule, longer_prod

        return rule, prod

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
            token = {
                'token': action,
                'value': raw[
                    self.stack[-rule_len]['start']:self.stack[-1]['end']],
                'start': self.stack[-rule_len]['start'],
                'end': self.stack[-1]['end']}
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

        valid_tokens = {t[0] for t in self.lexer.tokens}
        valid_tokens |= {v['action'] for k, v in self.rules.items()}

        errors = set()
        for rule, _ in self.rules.items():
            for token in rule.split():
                if token not in valid_tokens:
                    errors.add(f'"{token}"')

        if errors:
            raise ValueError(f'Unknown tokens: {", ".join(errors)}.')
