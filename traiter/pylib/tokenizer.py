"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""
import csv
import re
import string
from pathlib import Path
from typing import Optional

from spacy.lang.char_classes import ALPHA
from spacy.lang.char_classes import LIST_HYPHENS
from spacy.lang.char_classes import LIST_PUNCT
from spacy.lang.char_classes import LIST_QUOTES
from spacy.language import Language
from spacy.symbols import ORTH
from spacy.util import compile_infix_regex
from spacy.util import compile_prefix_regex
from spacy.util import compile_suffix_regex

from . import const as t_const
from .traits import us_location

BREAKING = LIST_QUOTES + LIST_PUNCT + [r"[:\\/˂˃×.+’()\[\]±_]"]

CLOSES = "|".join(re.escape(h) for h in t_const.CLOSE if len(h) == 1)
CLOSES = f"(?:{CLOSES})"

DASHES = "|".join(re.escape(h) for h in LIST_HYPHENS if len(h) == 1)
DASHES = f"(?:{DASHES})+"

OPENS = "|".join(re.escape(h) for h in t_const.OPEN if len(h) == 1)
OPENS = f"(?:{OPENS})"

PREFIX = BREAKING + [DASHES + "(?=[0-9])"]
SUFFIX = BREAKING + [DASHES]


INFIX = [
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


def append_prefix_regex(nlp: Language, prefixes: Optional[list[str]] = None):
    prefixes = prefixes if prefixes else []
    prefixes += nlp.Defaults.prefixes
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.prefix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: Optional[list[str]] = None):
    suffixes = suffixes if suffixes else []
    suffixes += nlp.Defaults.suffixes
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: Optional[list[str]] = None):
    infixes = infixes if infixes else []
    infixes += nlp.Defaults.infixes
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_abbrevs(nlp: Language, abbrevs: list[str]):
    for abbrev in abbrevs:
        nlp.tokenizer.add_special_case(abbrev, [{ORTH: abbrev}])


def remove_special_case(nlp: Language, remove: list[str]):
    """Remove special rules from the tokenizer.
    This is a workaround for when these special cases interfere with matcher rules.
    """
    specials = [r for r in nlp.tokenizer.rules if r not in remove]
    nlp.tokenizer.rules = None
    for text in specials:
        nlp.tokenizer.add_special_case(text, [{ORTH: text}])


def get_states():
    dir_ = Path(us_location.__file__).parent
    with open(dir_ / "us_location.csv") as in_file:
        reader = csv.DictReader(in_file)
        states = {t["pattern"] for t in reader if t["label"] == "us_state"}
    return states


def setup_tokenizer(nlp):
    append_prefix_regex(nlp, PREFIX)
    append_infix_regex(nlp, INFIX)
    append_suffix_regex(nlp, SUFFIX)
    append_abbrevs(nlp, ABBREVS)
    # Remove patterns that interfere with parses
    states = get_states()
    removes = []
    for rule in nlp.tokenizer.rules:
        if re.search(r"\d", rule) and not re.search(r"m\.?$", rule):
            removes.append(rule)
        if rule.lower() in states:
            removes.append(rule)
    remove_special_case(nlp, removes)
