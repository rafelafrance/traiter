"""Shared tokens for gonads (testes & ovaries)."""


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


texture = ('texture', ' smooth ')

# "covered"
covered = ('covered', ' covered ')

destroyed = ('destroyed', 'destroy(ed)?')


# Various size words
size = ('size', r"""
    ( very \s+ )?
    ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
        | extended | unobservable | sm-med
        | moderate | mod \b | medium  | med \b | minute | lg \b | sm \b | tiny )
    ( \s* size d? | [+] )?
    """)

# Forms of "developed"
developed = (
    'developed',
    r"""
        ( (fully | incompletely | partially | part | well) [.\s-]{0,2} )?""" +
    fr"""(developed? | undeveloped? | development | devel 
        | dev \b ([\s:]* none | {size[1]} )? 
        | undevel | undev | indist)
    """)

fat = ('fat', ' fat ')

# "Fully" or "incompletely"
fully = ('fully', ['fully', '( in )? complete ( ly )?'])

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

# Types of "visibility"
visible = ('visible', r""" ( very \s+ )? (
    visible | invisible | hidden | prominent? | seen | conspicuous | bare 
    ) """)

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

abdominal = ('abdominal', 'abdominal abdomin abdom abd'.split())

descended = ('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

# Other state words
other = (
    'other',
    'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

scrotal = ('scrotal', r'( scrotum | scrotal | scrot | nscr | scr) \b')

testes = ('testes', r' ( testes |  testis | testicles? | test ) \b ')


###############################################################################
# Female specific patterns

alb = ('alb', r' \b ( albicans | alb ) \b ')

corpus = ('corpus', r' \b ( corpus | corpora | corp | cor | c ) \b ')

fallopian = ('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

horns = ('horns', 'horns?')

lut = ('lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

ovary = ('ovary', r' ( ovary s? | ovaries | ov ) \b ')

uterus = ('uterus', 'uterus uterine ut'.split())

nipple = ('nipple', r""" ( \b
    nipples? | nipp?s? | teats? |
        ((mammae | mamm[ae]ry | mammaries | mamm) 
            (\s+ ( glands? | tisss?ue ) )? ) 
    ) \b """)

embryo = ('embryo', r"""
    embryonic | embryos? | embryps? | embroys | embs? | embrs? 
    | fetuses | fetus | foeti""")

# Spellings of placental scar
plac_scar = ('plac_scar', r"""
    ( placental | plac \b | postnatal | pac \b | \b pl \b ) 
        [.\s]* ( scarring | scars? )
    | p [\s.-] ( scarring | scars? )
    | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
    | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
    | ps \b | pslc | plac \b | plscr
    """)
