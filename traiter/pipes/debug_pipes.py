from spacy.language import Language

from traiter.pipes.pipe_util import add_extensions

DEBUG_TOKENS = "traiter.debug_tokens.v1"
DEBUG_ENTITIES = "traiter.debug_entities.v1"
DEBUG_MESSAGE = "traiter.debug_message.v1"

# So we don't have to come up with new names all the time
DEBUG_COUNT = 0  # Used to rename debug pipes


def tokens(nlp, message="", **kwargs):
    """Automatically setup a pipe to print token information."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {"message": message}
    nlp.add_pipe(
        DEBUG_TOKENS,
        name=f"debug_tokens_{DEBUG_COUNT}",
        config=config,
        **kwargs,
    )


def ents(nlp, message="", **kwargs):
    """Automatically setup a pipe to print entity information."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {"message": message}
    nlp.add_pipe(
        DEBUG_ENTITIES,
        name=f"debug_entities_{DEBUG_COUNT}",
        config=config,
        **kwargs,
    )


def msg(nlp, message="", **kwargs):
    """Automatically setup a pipe to print entity information."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {"message": message}
    nlp.add_pipe(
        DEBUG_MESSAGE,
        name=f"debug_message_{DEBUG_COUNT}",
        config=config,
        **kwargs,
    )


@Language.factory(DEBUG_TOKENS, default_config={"message": ""})
class DebugTokens:
    def __init__(self, nlp: Language, name: str, message: str = ""):
        add_extensions()
        self.nlp = nlp
        self.name = name
        self.message = message

    def __call__(self, doc):
        print("=" * 80)
        print(f"{self.name}: {self.message}")
        print(f'{"entity type":<20} {"dep":8} {"pos":6} {"cached label":<20} token')
        print(f'{"-----------":<20} {"---":8} {"---":6} {"------------":<20} -----')
        for token in doc:
            print(
                f"{token.ent_type_:<20} {token.dep_:8} {token.pos_:6} "
                f"{token._.cached_label:<20} {token}"
            )
        print()
        return doc


@Language.factory(DEBUG_ENTITIES, default_config={"message": ""})
class DebugEntities:
    def __init__(self, nlp: Language, name: str, message: str = ""):
        add_extensions()
        self.nlp = nlp
        self.name = name
        self.message = message

    def __call__(self, doc):
        print("=" * 80)
        print(f"{self.name}: {self.message}")
        for ent in doc.ents:
            print(f"{ent.label_:<20} {ent}")
            print(f'{" " * 20} {ent._.data}\n')
        print()
        return doc


@Language.factory(DEBUG_MESSAGE, default_config={"message": ""})
class DebugMessage:
    def __init__(self, nlp: Language, name: str, message: str = ""):
        add_extensions()
        self.nlp = nlp
        self.name = name
        self.message = message

    def __call__(self, doc):
        print("=" * 80)
        print(f"{self.name}: {self.message}")
        return doc
