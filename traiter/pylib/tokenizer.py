import string
from typing import Callable

import regex as re
from spacy.util import registry

from . import tokenizer_util
from .patterns import date_

ABBREVS = """
    Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
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
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

TOKENIZER = "traiter.custom_tokenizer.v1"

INFIX = [
    r"(?<=[0-9])[/,](?=[0-9])",  # digit,digit
    r"(?<=[A-Z])[/-](?=[0-9])",  # letter-digit
    "-_",
]


def setup_tokenizer(nlp):
    not_letter = re.compile(r"[^A-Za-z.']")
    removes = [{"pattern": s} for s in nlp.tokenizer.rules if not_letter.search(s)]
    tokenizer_util.remove_special_case(nlp, removes)
    tokenizer_util.remove_special_case(nlp, date_.DATE_TERMS)

    tokenizer_util.append_prefix_regex(nlp)
    tokenizer_util.append_infix_regex(nlp, INFIX)
    tokenizer_util.append_suffix_regex(nlp)

    tokenizer_util.append_abbrevs(nlp, ABBREVS)


@registry.callbacks(TOKENIZER)
def make_customized_tokenizer(tokenizer_setup: Callable = None):
    tokenizer_setup = tokenizer_setup if tokenizer_setup else setup_tokenizer

    def customized_tokenizer(nlp):
        tokenizer_setup(nlp)

    return customized_tokenizer
