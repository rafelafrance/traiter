"""Shared reproductive trait tokens (testes & ovaries)."""


from stacked_regex.rule import Rule, fragment, keyword


REPRODUCTIVE = {}


def add(rule: Rule) -> None:
    """Add a rule to SHARED."""
    REPRODUCTIVE[rule.name] = rule


add(keyword('active', 'active inactive'.split()))
add(fragment('and', r' ( and \b | [&] ) '))
add(keyword('count', r"""( only | all | both )? \s* [12]"""))

add(keyword(
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """))

add(keyword('texture', ' smooth '))

add(keyword('covered', ' covered '))

add(keyword('destroyed', 'destroy(ed)?'))

add(fragment('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b
        | sm \b | tiny )
    ( \s* size d? | [+] )?
    """))

add(fragment(
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well)
            [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel
        | dev \b ([\s:]* none | {REPRODUCTIVE['size'].pattern} )?
        | undevel | undev | indist)
    """))

add(keyword('fat', ' fat '))

add(fragment('fully', ['fully', '( in )? complete ( ly )?']))

add(fragment('gonads', ' (?P<ambiguous_key> gonads? ) '))

add(fragment('in', r' in '))

add(keyword('label', 'reproductive .? ( data | state | condition )'))

add(fragment('mature', r'( immature | mature | imm ) \b '))

add(fragment('non', r' \b ( not | non | no | semi | sub ) '))
add(fragment('none', r' \b ( no | none | not | non ) \b '))

add(fragment(
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split()))

add(fragment('sep', ' [;] | $ '))

add(fragment('sign', ' [+-] '))

add(keyword('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous
        | bare
    ) """))

# We allow random words in some situations
add(fragment('word', ' [a-z]+ '))

add(keyword('tissue', ' tissue '.split()))

add(keyword('present', ' present absent '.split()))

# The sides like: 3L or 4Right
add(fragment('side', r"""
    left | right | lf | lt | rt | [lr] (?! [a-z] ) """))

# Some traits are presented as an equation
add(fragment('op', r' [+:&] '))
add(fragment('eq', r' [=] '))

add(fragment('abdominal', 'abdominal abdomin abdom abd'.split()))

add(fragment('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )']))

# Other state words
add(keyword(
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split()))

add(fragment(
    'scrotal', r'( scrotum | scrotal | scrot | nscr | scr) \b'))

add(fragment(
    'testes', r' ( testes |  testis | testicles? | test ) \b '))

add(fragment('alb', r' \b ( albicans | alb ) \b '))

add(fragment(
    'corpus', r' \b ( corpus | corpora | corp | cor | c ) \b '))

add(fragment('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? '))

add(keyword('horns', 'horns?'))

add(fragment(
    'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b '))

add(fragment('ovary', r' ( ovary s? | ovaries | ov ) \b '))

add(fragment('uterus', 'uterus uterine ut'.split()))

add(fragment('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm)
            (\s+ ( glands? | tisss?ue ) )? )
    ) \b """))

add(fragment('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs?
    | fetuses | fetus | foeti"""))

# Spellings of placental scar
add(fragment('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b )
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """))


# Gonads can be for female or male
add(fragment('ambiguous_key', r' gonads? '))
