"""Add a pipe to print debug messages."""

from spacy.language import Language

from traiter.pipes.entity_data import add_extensions

DEBUG_TOKENS = 'debug_tokens.v1'
DEBUG_ENTITIES = 'debug_entities.v1'

add_extensions()

DEBUG_COUNT = 0  # Used to rename debug pipes


def rename(name: str):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    return f'{name}_{DEBUG_COUNT}'


@Language.factory(DEBUG_TOKENS, default_config={'message': ''})
class DebugTokens:
    """Print debug messages."""

    def __init__(self, nlp: Language, name: str, message: str = ''):
        self.nlp = nlp
        self.name = rename(name)
        self.message = message

    def __call__(self, doc):
        print('=' * 80)
        print(f'{self.name}: {self.message}')
        for token in doc:
            print(f'{token.ent_type_:<20} {token.dep_:8} {token.pos_:6} '
                  f'{token._.cached_label:<20} {token}')
        print()
        return doc


@Language.factory(DEBUG_ENTITIES, default_config={'message': ''})
class DebugEntities:
    """Print debug messages."""

    def __init__(self, nlp: Language, name: str, message: str = ''):
        self.nlp = nlp
        self.name = rename(name)
        self.message = message

    def __call__(self, doc):
        print('=' * 80)
        print(f'{self.name}: {self.message}')
        for ent in doc.ents:
            print(f'{ent.label_:<20} {ent}')
            print(f'{" " * 20} {ent._.data}\n')
        print()
        return doc
