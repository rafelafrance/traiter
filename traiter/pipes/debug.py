"""Add a pipe to print debug messages."""

from spacy.language import Language

DEBUG_TOKENS = 'debug_tokens'
DEBUG_ENTITIES = 'debug_entities'


@Language.factory(DEBUG_TOKENS)
def debug_tokens(nlp: Language, name: str, message: str):
    """Print debug messages."""
    return DebugTokens(message)


class DebugTokens:
    """Print debug messages."""

    def __init__(self, message):
        self.message = message

    def __call__(self, doc):
        print('=' * 80)
        print(f'tokens: {self.message}')
        for token in doc:
            print(f'{token.ent_type_:<20} {token.dep_:8} {token.pos_:6} '
                  f'{token._.cached_label:<20} {token}')
        print()
        return doc


@Language.factory(DEBUG_ENTITIES)
def debug_entities(nlp: Language, name: str, message: str):
    """Print debug messages."""
    return DebugEntities(message)


class DebugEntities:
    """Print debug messages."""

    def __init__(self, message):
        self.message = message

    def __call__(self, doc):
        print('=' * 80)
        print(f'entities: {self.message}')
        for ent in doc.ents:
            print(f'{ent.label_:<20} {ent}')
            print(f'{" " * 20} {ent._.data}\n')
        print()
        return doc
