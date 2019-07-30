"""Shared tokens for gonads (testes & ovaries)."""


# Forms of "active"
active = ('active', 'active inactive'.split())

# Links gonads and other related traits
and_ = ('and', r' ( and | [&] ) \b ')

# A count
count_ = ('count', r"""( only | all | both )? \s* [12]""")

# Colors associated with gonads
color = ('color', r' ( dark | light | pale )? \s* ( red | pink ) ')

# "covered"
covered = ('covered', ' covered ')

# Forms of "destroyed"
destroyed = ('destroyed', 'destroy(ed)?')

# Forms of "developed"
developed = ('developed', r"""
    (fully | incompletely | partially | part)?
    [.\s-]{0,2}
    (developed | undeveloped | devel | undevel | undev)
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

# Spellings of "partially"
partially = ('partially', ['partially', r' \b part \b', r'\b pt \b'])

# Some patterns require a separator
sep = ('sep', ' [;] | $ ')

# Sign for presence or absence
sign = ('sign', ' [+-] ')

# Various size words
size = ('size', r"""
    ( enlarged | enlarge | large | small | shrunken | shrunk 
        | moderate | mod | minute )      
    ( \s* size d? )?
    """)

# Types of "visibility"
visible = ('visible', 'visible invisible hidden prominent'.split())

# We allow random words in some situations
word = ('word', ' [a-z]+ ')


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

# Various spellings of "testes"
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

# Various spellings of ovary
ovary = ('ovary', r' ( ovary s? | ovaries | ov ) \b ')

# Various spellings of uterus
uterus = ('uterus', 'uterus uterine'.split())
