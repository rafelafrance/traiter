"""Shared reproductive trait tokens (testes & ovaries)."""


from pylib.stacked_regex.rule import fragment, keyword, InRegexp


REPRODUCTIVE = {}


def add_frag(name: str, regexp: InRegexp) -> None:
    """Add a rule to REPRODUCTIVE."""
    REPRODUCTIVE[name] = fragment(name, regexp)


def add_key(name: str, regexp: InRegexp) -> None:
    """Add a rule to REPRODUCTIVE."""
    REPRODUCTIVE[name] = keyword(name, regexp)


add_key('active', 'active inactive'.split())
add_frag('and', r' ( and \b | [&] ) ')
add_key('count', r"""( only | all | both )? \s* [12]""")

add_key(
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """)

add_key('texture', ' smooth ')

add_key('covered', ' covered ')

add_key('destroyed', 'destroy(ed)?')

add_frag('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b
        | sm \b | tiny )
    ( \s* size d? | [+] )?
    """)

add_frag(
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well)
            [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel
        | dev \b ([\s:]* none | {REPRODUCTIVE['size'].pattern} )?
        | undevel | undev | indist)
    """)

add_key('fat', ' fat ')

add_frag('fully', ['fully', '( in )? complete ( ly )?'])

add_frag('gonads', ' (?P<ambiguous_key> gonads? ) ')

add_frag('in', r' in ')

add_key('label', 'reproductive .? ( data | state | condition )')

add_frag('mature', r'( immature | mature | imm ) \b ')

add_frag('non', r' \b ( not | non | no | semi | sub ) ')
add_frag('none', r' \b ( no | none | not | non ) \b ')

add_frag(
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split())

add_frag('sep', ' [;] | $ ')

add_frag('sign', ' [+-] ')

add_key('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous
        | bare
    ) """)

# We allow random words in some situations
add_frag('word', ' [a-z]+ ')

add_key('tissue', ' tissue '.split())

add_key('present', ' present absent '.split())

# The sides like: 3L or 4Right
add_frag('side', r"""
    left | right | lf | lt | rt | [lr] (?! [a-z] ) """)

# Some traits are presented as an equation
add_frag('op', r' [+:&] ')
add_frag('eq', r' [=] ')

add_frag('abdominal', 'abdominal abdomin abdom abd'.split())

add_frag('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
add_key(
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

add_frag(
    'scrotal', r'( scrotum | scrotal | scrot | nscr | scr) \b')

add_frag(
    'testes', r' ( testes |  testis | testicles? | test ) \b ')

add_frag('alb', r' \b ( albicans | alb ) \b ')

add_frag(
    'corpus', r' \b ( corpus | corpora | corp | cor | c ) \b ')

add_frag('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

add_key('horns', 'horns?')

add_frag(
    'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

add_frag('ovary', r' ( ovary s? | ovaries | ov ) \b ')

add_frag('uterus', 'uterus uterine ut'.split())

add_frag('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm)
            (\s+ ( glands? | tisss?ue ) )? )
    ) \b """)

add_frag('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs?
    | fetuses | fetus | foeti """)

# Spellings of placental scar
add_frag('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b )
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """)


# Gonads can be for female or male
add_frag('ambiguous_key', r' gonads? ')
