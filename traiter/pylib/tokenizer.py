import re
import string

from spacy.lang.char_classes import ALPHA
from spacy.lang.char_classes import LIST_HYPHENS
from spacy.lang.char_classes import LIST_PUNCT
from spacy.lang.char_classes import LIST_QUOTES

from .vocabulary import terms
from traiter.pylib import const as t_const
from traiter.pylib import tokenizer_util

BREAKING = LIST_QUOTES + LIST_PUNCT + [r"[:\\/˂˃×.+’()\[\]±_]"]

CLOSES = "|".join(re.escape(h) for h in t_const.CLOSE if len(h) == 1)
CLOSES = f"(?:{CLOSES})"

DASHES = "|".join(re.escape(h) for h in LIST_HYPHENS if len(h) == 1)
DASHES = f"(?:{DASHES})+"

OPENS = "|".join(re.escape(h) for h in t_const.OPEN if len(h) == 1)
OPENS = f"(?:{OPENS})"

_PREFIX = BREAKING + [DASHES + "(?=[0-9])"]
_SUFFIX = BREAKING + [DASHES]


_INFIX = [
    rf"(?<=[{ALPHA}0-9])[:<>=/+](?=[{ALPHA}])",  # word=word etc.
    r"""[\\\[\]()/:;’'"“”'+±_]""",  # Break on these characters
    DASHES,
    rf"(?<=\d)[{ALPHA}]+",
]

# Abbreviations commonly found in treatments relating to plants
PDF_ABBREVS = """
    Acad. adj. Af. Agri. al. alt. Amer. Ann. ann. Arb. Arch. Arq.
    Bol. Bot. bot. Bras. bras. Bull.
    c. ca. Cat. cent. centr. cf. Ci. cit. Coll. coll. Columb. Com. com. Contr. Cur.
    DC. Dept. depto. Diam. diam. Distr. distr. dtto.
    e. e.g. ed. eg. ememd. Encycl. Encyle. ent. Est. est. Exot.
    FIG. Fig. fig. Figs. figs. Fl. fl. flor. flumin. frag.
    g. Gard. gard. Gen. Geo. geograph.
    hb. Herb. Hist. hist. Hort.
    illeg. Ind. infra. Is. is.
    Jahrb. Jard. Jr. jug.
    Lab. Lam. lam. lat. Leg. leg. Legum. lin. Linn. loc. long.
    Mag. Mem. mem. mens. Mex. Mim.
    monac. mont. Mts. Mun. mun. Mus.
    Nac. Nat. nat. Natl. Neg. No. no. nom. nud.
    Ocas.
    p. photo. PI. pi. PL. Pl. pl. pr. Proc. Prodr. Prov. prov. Pt. Pto. Publ.
    reg. Rev. revis.
    s. Sa. Sci. sci. Ser. Soc. Spec. Spp. spp. Sr. ST. St. Sta. stat. stk. Sto. str.
    Sul. superfl. Suppl. suppl. surv. syn. Syst.
    t. tab. telegr. Tex. Trans Trans.
    U.S. Univ. US.
    Veg. veg.
    Wm.
    I. II. III. IV. IX. V. VI. VII. VIII. X. XI. XII. XIII. XIV. XIX. XV. XVI. XVII.
    XVIII. XX. XXI. XXII. XXIII. XXIV. XXV.
    i. ii. iii. iv. ix. v. vi. vii. viii. x. xi. xii. xiii. xiv. xix. xv. xvi. xvii.
    xviii. xx. xxi. xxii. xxiii. xxiv. xxv.
    """.split()

ABBREVS = """
    Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

STATES = [t["pattern"] for t in terms.ADMIN_UNIT_TERMS.pick("us_state")]


def setup_tokenizer(nlp):
    tokenizer_util.append_prefix_regex(nlp, _PREFIX)
    tokenizer_util.append_infix_regex(nlp, _INFIX)
    tokenizer_util.append_suffix_regex(nlp, _SUFFIX)
    tokenizer_util.append_abbrevs(nlp, ABBREVS)
    # Remove patterns that interfere with parses
    removes = []
    for rule in nlp.tokenizer.rules:
        if re.search(r"\d", rule) and not re.search(r"m\.?$", rule):
            removes.append(rule)
        if rule.lower() in STATES:
            removes.append(rule)
    tokenizer_util.remove_special_case(nlp, removes)
