"""Parse the notations."""


class BaseParser:
    """Shared parser logic."""

    def __init__(self, lexer):
        """Initialize the parser."""
        self.lexer = lexer()
        self.rules = {' '.join(k.split()): v
                      for k, v in self.get_rules().items()}
        self.max = max(len(k.split()) for k, v in self.rules.items())

    def get_rules(self):
        return {
            'number to number': self.range,
        }

    def parse(self, input):
        """Parse the tokens."""
        tokens = self.lexer.tokenize(input)
        if not tokens:
            return []

        stack = []
        results = []
        tokens.append({'token': 'END', 'value': None, 'start': 0, 'end': 0})

        while tokens:
            if not stack:
                stack.append(tokens.pop(0))
                continue

            count = min(len(stack), self.max)
            for i in stack:
                print(i)

            for j in range(count, 0, -1):
                key = ' '.join([t['token'] for t in stack[-j:]])
                print('key=', key)
                production = self.rules.get(key)

                if callable(production):
                    print('callable')
                    results.append(production(stack[-j:], input))
                    del stack[-j:]
                    break
                elif production:
                    print('replace')
                    token = {
                        'token': production,
                        'value': input[stack[-j]['start']:stack[-1]['end']],
                        'start': stack[-j]['start'],
                        'end': stack[-1]['end'],
                    }
                    del stack[-j:]
                    stack.append(token)
                    break
            else:
                print('shift')
                stack.append(tokens.pop(0))
            print()

        return results

    def range(self, stack, input):
        return
