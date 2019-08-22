"""Shared tokens for gonads (testes & ovaries)."""


# Forms of "active"
active = ('active', 'active inactive'.split())

# Links gonads and other related traits
and_ = ('and', r' ( and \b | [&] ) ')

# A count
count_ = ('count', r"""( only | all | both )? \s* [12]""")

# Colors associated with gonads
color = (
    'color',
    r""" (( dark | light | pale ) \s* )?
         ( red | pink | brown | black | white | pigmented ) """)

# "covered"
covered = ('covered', ' covered ')

# Forms of "destroyed"
destroyed = ('destroyed', 'destroy(ed)?')

# Forms of "developed"
developed = ('developed', r"""
    (fully | incompletely | partially | part | well)?
    [.\s-]{0,2}
    (developed? | undeveloped? | development | devel 
        | undevel | undev | indist)
    """)

# "fat"
fat = ('fat', ' fat ')

# "Fully" or "incompletely"
fully = ('fully', ['fully', '( in )? complete ( ly )?'])

# Spellings of "gonads"
gonads = ('gonads', ' (?P<ambiguous_key> gonads? ) ')

# Links gonads and other related traits
in_ = ('in', r' in ')

# A label, like: "reproductive data"
label = ('label', 'reproductive .? ( data | state | condition )')

# Forms of "maturity"
mature = ('mature', r'( immature | mature | imm ) \b ')

# Negation: "non", "not", etc.
non = ('non', r' \b ( not | non | no | semi | sub ) ')
none = ('none', r' \b ( no | none | not | non ) \b ')

# Spellings of "partially"
partially = (
    'partially',
    ['partially', r' \b part \b', r'\b pt \b']
    + 'slightly slight '.split())

# Some patterns require a separator
sep = ('sep', ' [;] | $ ')

# Sign for presence or absence
sign = ('sign', ' [+-] ')

# Various size words
size = ('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | moderate | mod | minute | lg | sm | tiny )
    ( \s* size d? )?
    """)

# Types of "visibility"
visible = ('visible', """
    visible invisible hidden prominent seen conspicuous""".split())

# We allow random words in some situations
word = ('word', ' [a-z]+ ')

tissue = ('tissue', ' tissue '.split())

present = ('present', ' present absent '.split())

# The sides like: 3L or 4Right
side = ('side', r""" left | right | lf | lt | rt | [lr] (?! [a-z] ) """)

# Some traits are presented as an equation
op = ('op', r' [+:&] ')
eq = ('eq', r' [=] ')

###############################################################################
# Male specific patterns

# Spellings of abdominal
abdominal = ('abdominal', 'abdominal abdomin abdom abd'.split())

# "Descended"
descended = ('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
other = (
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

# Spellings of "scrotum"
scrotal = ('scrotal', r'( scrotum | scrotal | scrot | nscr | scr) \b')

# Spellings of "testes"
testes = ('testes', r' ( testes |  testis | testicles? | test ) \b ')


###############################################################################
# Female specific patterns

# Spellings of albicans
alb = ('alb', r' \b ( albicans | alb ) \b ')

# Spellings of corpus
corpus = ('corpus', r' \b ( corpus | corpora | corp | cor | c ) \b ')

# Various forms of fallopian tubes
fallopian = ('fallopian', r' fallopian ( \s* tubes? )? ')

# Words related to ovaries
horns = ('horns', 'horns?')

# Spellings of luteum
lut = ('lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

# Spellings of ovary
ovary = ('ovary', r' ( ovary s? | ovaries | ov ) \b ')

# Spellings of uterus
uterus = ('uterus', 'uterus uterine'.split())

# Spellings of nipple
nipple = ('nipple', r"""
    nipples? | nipp?s? | teats? |
        ((mammae | mammary | mammaries | mamm) 
            (\s+ ( glands? | tisss?ue ) )? ) """)

# Spellings of embryo
embryo = ('embryo', r"""
    embryos? | embryps? | embroys | embryonic | embs? | embrs? 
    | fetuses | fetus | foeti""")

# Spellings of placental scar
plac_scar = ('plac_scar', r"""
    ( placental | plac | postnatal | pac ) [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? )
    | ps | pslc | plac | plscr
    """)
