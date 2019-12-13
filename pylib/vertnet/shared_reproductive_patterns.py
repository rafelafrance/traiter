"""Shared reproductive trait tokens (testes & ovaries)."""

import pylib.vertnet.shared_patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog


SET = RuleCatalog(patterns.CAT)
RULE = SET.rules


SET.term('active', 'active inactive'.split())
SET.part('and', r' ( and \b | [&] ) ')
SET.term('count', r"""( only | all | both )? \s* [12]""")

SET.term(
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """)

SET.term('texture', ' smooth ')

SET.term('covered', ' covered ')

SET.term('destroyed', 'destroy(ed)?')

SET.part('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b
        | sm \b | tiny )
    ( \s* size d? | [+] )?
    """)

SET.part(
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well)
            [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel
        | dev \b ([\s:]* none | {RULE['size'].pattern} )?
        | undevel | undev | indist)
    """)

SET.term('fat', ' fat ')

SET.part('fully', ['fully', '( in )? complete ( ly )?'])

SET.part('gonads', ' (?P<ambiguous_key> gonads? ) ')

SET.part('in', r' in ')

SET.term('label', 'reproductive .? ( data | state | condition )')

SET.part('mature', r'( immature | mature | imm ) \b ')

SET.part('non', r' \b ( not | non | no | semi | sub ) ')
SET.part('none', r' \b ( no | none | not | non ) \b ')

SET.part(
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split())

SET.part('sep', ' [;] | $ ')

SET.part('sign', ' [+-] ')

SET.term('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous
        | bare
    ) """)

# We allow random words in some situations
SET.part('word', ' [a-z]+ ')

SET.term('tissue', ' tissue '.split())

SET.term('present', ' present absent '.split())

# Some traits are presented as an equation
SET.part('op', r' [+:&] ')
SET.part('eq', r' [=] ')

SET.part('abdominal', 'abdominal abdomin abdom abd'.split())

SET.part('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
SET.term(
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

SET.part(
    'scrotal', r'( nonscrotal | scrotum | scrotal | scrot | nscr | scr) \b')

SET.part(
    'testes', r' ( testes |  testis | testicles? | test ) \b ')

SET.part('alb', r' \b ( albicans | alb ) \b ')

SET.part('corpus', r"""
    \b ( c\.l\. | ( corpus | corpora | corp | cor | c | cl ) \b )""")

SET.part('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

SET.term('horns', 'horns?')

SET.part(
    'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

SET.part('ovary', r' ( ovary s? | ovaries | ov ) \b ')

SET.part('uterus', 'uterus uterine ut'.split())

SET.part('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm)
            (\s+ ( glands? | tisss?ue ) )? )
    ) \b """)

SET.part('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs?
    | fetuses | fetus | foeti """)

# Spellings of placental scar
SET.part('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b )
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """)

# Gonads can be for female or male
SET.part('ambiguous_key', r' gonads? ')
