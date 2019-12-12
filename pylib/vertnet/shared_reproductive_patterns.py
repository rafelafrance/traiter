"""Shared reproductive trait tokens (testes & ovaries)."""

import pylib.vertnet.shared_patterns as patterns
from pylib.shared.rule_set import RuleSet


SET = RuleSet(patterns.SET)
RULE = SET.rules


SET.add_key('active', 'active inactive'.split())
SET.add_frag('and', r' ( and \b | [&] ) ')
SET.add_key('count', r"""( only | all | both )? \s* [12]""")

SET.add_key(
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """)

SET.add_key('texture', ' smooth ')

SET.add_key('covered', ' covered ')

SET.add_key('destroyed', 'destroy(ed)?')

SET.add_frag('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b
        | sm \b | tiny )
    ( \s* size d? | [+] )?
    """)

SET.add_frag(
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well)
            [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel
        | dev \b ([\s:]* none | {RULE['size'].pattern} )?
        | undevel | undev | indist)
    """)

SET.add_key('fat', ' fat ')

SET.add_frag('fully', ['fully', '( in )? complete ( ly )?'])

SET.add_frag('gonads', ' (?P<ambiguous_key> gonads? ) ')

SET.add_frag('in', r' in ')

SET.add_key('label', 'reproductive .? ( data | state | condition )')

SET.add_frag('mature', r'( immature | mature | imm ) \b ')

SET.add_frag('non', r' \b ( not | non | no | semi | sub ) ')
SET.add_frag('none', r' \b ( no | none | not | non ) \b ')

SET.add_frag(
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split())

SET.add_frag('sep', ' [;] | $ ')

SET.add_frag('sign', ' [+-] ')

SET.add_key('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous
        | bare
    ) """)

# We allow random words in some situations
SET.add_frag('word', ' [a-z]+ ')

SET.add_key('tissue', ' tissue '.split())

SET.add_key('present', ' present absent '.split())

# Some traits are presented as an equation
SET.add_frag('op', r' [+:&] ')
SET.add_frag('eq', r' [=] ')

SET.add_frag('abdominal', 'abdominal abdomin abdom abd'.split())

SET.add_frag('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
SET.add_key(
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

SET.add_frag(
    'scrotal', r'( nonscrotal | scrotum | scrotal | scrot | nscr | scr) \b')

SET.add_frag(
    'testes', r' ( testes |  testis | testicles? | test ) \b ')

SET.add_frag('alb', r' \b ( albicans | alb ) \b ')

SET.add_frag('corpus', r"""
    \b ( c\.l\. | ( corpus | corpora | corp | cor | c | cl ) \b )""")

SET.add_frag('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

SET.add_key('horns', 'horns?')

SET.add_frag(
    'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

SET.add_frag('ovary', r' ( ovary s? | ovaries | ov ) \b ')

SET.add_frag('uterus', 'uterus uterine ut'.split())

SET.add_frag('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm)
            (\s+ ( glands? | tisss?ue ) )? )
    ) \b """)

SET.add_frag('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs?
    | fetuses | fetus | foeti """)

# Spellings of placental scar
SET.add_frag('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b )
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """)

# Gonads can be for female or male
SET.add_frag('ambiguous_key', r' gonads? ')
