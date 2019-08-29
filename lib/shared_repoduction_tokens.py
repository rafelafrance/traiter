"""Shared reproductive trait tokens (testes & ovaries)."""


from stacked_regex.rule_builder import RuleBuilder


class ReproductiveTokens(RuleBuilder):
    """Build common reproductive trait tokens."""

    def __init__(self):
        """Build the stacked regular expressions."""
        super().__init__()

        self.keyword('active', 'active inactive'.split())
        self.fragment('and', r' ( and \b | [&] ) ')
        self.keyword('count', r"""( only | all | both )? \s* [12]""")

        self.keyword(
            'color',
            r""" (( dark | light | pale ) \s* )?
                 ( red | pink | brown | black | white | pigmented ) """)

        self.keyword('texture', ' smooth ')

        self.keyword('covered', ' covered ')

        self.keyword('destroyed', 'destroy(ed)?')

        self.fragment('size', r"""
            ( very \s+ )?
            ( enlarged | enlarge | large | small | shrunken | shrunk | swollen
                | extended | unobservable | sm-med
                | moderate | mod \b | medium  | med \b | minute | lg \b 
                | sm \b | tiny )
            ( \s* size d? | [+] )?
            """)

        self.fragment(
            'developed',
            r"""
                ( (fully | incompletely | partially | part | well)
                    [.\s-]{0,2} )?""" +
            fr"""(developed? | undeveloped? | development | devel
                | dev \b ([\s:]* none | {self['size'].pattern} )?
                | undevel | undev | indist)
            """)

        self.keyword('fat', ' fat ')

        self.fragment('fully', ['fully', '( in )? complete ( ly )?'])

        self.fragment('gonads', ' (?P<ambiguous_key> gonads? ) ')

        self.fragment('in', r' in ')

        self.keyword('label', 'reproductive .? ( data | state | condition )')

        self.fragment('mature', r'( immature | mature | imm ) \b ')

        self.fragment('non', r' \b ( not | non | no | semi | sub ) ')
        self.fragment('none', r' \b ( no | none | not | non ) \b ')

        self.fragment(
            'partially',
            ['partially', r' \b part \b', r'\b pt \b']
            + 'slightly slight '.split())

        self.fragment('sep', ' [;] | $ ')

        self.fragment('sign', ' [+-] ')

        self.keyword('visible', r""" ( very \s+ )? (
            visible | invisible | hidden | prominent? | seen | conspicuous 
                | bare 
            ) """)

        # We allow random words in some situations
        self.fragment('word', ' [a-z]+ ')

        self.keyword('tissue', ' tissue '.split())

        self.keyword('present', ' present absent '.split())

        # The sides like: 3L or 4Right
        self.fragment('side', r"""
            left | right | lf | lt | rt | [lr] (?! [a-z] ) """)

        # Some traits are presented as an equation
        self.fragment('op', r' [+:&] ')
        self.fragment('eq', r' [=] ')

        #######################################################################
        # Male specific patterns

        self.fragment('abdominal', 'abdominal abdomin abdom abd'.split())

        self.fragment('descended', ['( un )? ( des?c?end ( ed )?', 'desc? )'])

        # Other state words
        self.keyword(
            'other',
            'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

        self.fragment(
            'scrotal', r'( scrotum | scrotal | scrot | nscr | scr) \b')

        self.fragment(
            'testes', r' ( testes |  testis | testicles? | test ) \b ')

        #######################################################################
        # Female specific patterns

        self.fragment('alb', r' \b ( albicans | alb ) \b ')

        self.fragment(
            'corpus', r' \b ( corpus | corpora | corp | cor | c ) \b ')

        self.fragment('fallopian', r' ( fallopian | foll ) ( \s* tubes? )? ')

        self.keyword('horns', 'horns?')

        self.fragment(
            'lut', r' ( c \.? l \.\? ) | \b ( luteum | lute | lut ) \b ')

        self.fragment('ovary', r' ( ovary s? | ovaries | ov ) \b ')

        self.fragment('uterus', 'uterus uterine ut'.split())

        self.fragment('nipple', r""" ( \b
            nipples? | nipp?s? | teats? |
                ((mammae | mamm[ae]ry | mammaries | mamm) 
                    (\s+ ( glands? | tisss?ue ) )? ) 
            ) \b """)

        self.fragment('embryo', r"""
            embryonic | embryos? | embryps? | embroys | embs? | embrs? 
            | fetuses | fetus | foeti""")

        # Spellings of placental scar
        self.fragment('plac_scar', r"""
            ( placental | plac \b | postnatal | pac \b | \b pl \b ) 
                [.\s]* ( scarring | scars? )
            | p [\s.-] ( scarring | scars? )
            | ( uterus | uterine | \b ut \b ) [.\s]* ( scarring | scars? )
            | ( scarring | scars? ) \b (?! \s* ( on | above | below ) )
            | ps \b | pslc | plac \b | plscr
            """)
