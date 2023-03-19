"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""
from typing import Iterable
from typing import Optional

from spacy.language import Language
from spacy.symbols import ORTH
from spacy.util import compile_infix_regex
from spacy.util import compile_prefix_regex
from spacy.util import compile_suffix_regex

ABBREVS = """
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


def append_abbrevs(nlp: Language, special_cases: list[str]):
    """Add special case tokens to the tokenizer."""
    for case in special_cases:
        nlp.tokenizer.add_special_case(case, [{ORTH: case}])


def add_special_case(nlp: Language, special_cases: list[Iterable]):
    """Add special case tokens to the tokenizer."""
    for case in special_cases:
        text, *parts = case
        rule = [{ORTH: p} for p in parts]
        nlp.tokenizer.add_special_case(text, rule)


def remove_special_case(nlp: Language, remove: list[dict]):
    """Remove special rules from the tokenizer.
    This is a workaround for when these special cases interfere with matcher rules.
    """
    remove = {r["pattern"].lower() for r in remove}
    specials = [(r, r) for r in nlp.tokenizer.rules if r.lower() not in remove]
    nlp.tokenizer.rules = None
    add_special_case(nlp, specials)
