"""Shared reproductive trait tokens (testes & ovaries)."""

import pylib.vertnet.shared_patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST

CATALOG = RuleCatalog(patterns.CATALOG)

CATALOG.term('active', 'active inactive'.split())
CATALOG.part('and', r' ( and \b | [&] ) ')
CATALOG.term('count', r"""( only | all | both )? \s* [12]""")

CATALOG.term(
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """)

CATALOG.term('texture', ' smooth ')

CATALOG.term('covered', ' covered ')

CATALOG.term('destroyed', 'destroy(ed)?')

CATALOG.part('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b
        | sm \b | tiny )
    ( \s* size d? | [+] )?
    """)

CATALOG.part(
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well)
            [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel
        | dev \b ([\s:]* none | {CATALOG['size'].pattern} )?
        | undevel | undev | indist)
    """)

CATALOG.term('fat', ' fat ')

CATALOG.part('fully', ['fully', '( in )? complete ( ly )?'])

CATALOG.part('gonads', ' (?P<ambiguous_key> gonads? ) ')

CATALOG.part('in', r' in ')

CATALOG.term('label', 'reproductive .? ( data | state | condition )')

CATALOG.part('mature', r'( immature | mature | imm ) \b ')

CATALOG.part('non', r' \b ( not | non | no | semi | sub ) ')
CATALOG.part('none', r' \b ( no | none | not | non ) \b ')

CATALOG.part(
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split())

CATALOG.part('sep', ' [;] | $ ')

CATALOG.part('sign', ' [+-] ')

CATALOG.term('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous
        | bare | faint | definite
    ) """)

# We allow random words in some situations
CATALOG.part('word', ' [a-z]+ ', capture=False, when=LAST)

CATALOG.term('tissue', ' tissue '.split())

CATALOG.term('present', ' present absent '.split())

# Some traits are presented as an equation
CATALOG.part('op', r' [+:&] ')
CATALOG.part('eq', r' [=] ')

CATALOG.part('abdominal', 'abdominal abdomin abdom abd'.split())

CATALOG.part('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
CATALOG.term(
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

CATALOG.part(
    'scrotal', r'( nonscrotal | scrotum | scrotal | scrot | nscr | scr) \b')

CATALOG.part(
    'testes', r' ( testes |  testis | testicles? | test ) \b ')

CATALOG.part('alb', r' \b ( albicans | alb ) \b ')

CATALOG.part('corpus', r"""
    \b ( c\.l\. | ( corpus | corpora | corp | cor | c | cl ) \b )""")

CATALOG.part('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

CATALOG.term('horns', 'horns?')

CATALOG.part(
    'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

CATALOG.part('ovary', r' ( ovary s? | ovaries | ov ) \b ')

CATALOG.part('uterus', 'uterus uterine ut'.split())

CATALOG.part('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm)
            (\s+ ( glands? | tisss?ue ) )? )
    ) \b """)

CATALOG.part('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs?
    | fetuses | fetus | foeti """)

# Spellings of placental scar
CATALOG.part('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b )
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """)

# Gonads can be for female or male
CATALOG.part('ambiguous_key', r' gonads? ')
