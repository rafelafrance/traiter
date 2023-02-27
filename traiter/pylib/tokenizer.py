import string

import regex as re
from spacy.util import registry

from traiter.pylib import tokenizer_util

ABBREVS = """
    Jan. Feb. Febr. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
    Acad. Af. Agri. Amer. Ann. Arb. Arch. Arq. adj. al. alt. ann.
    Bol. Bot. Bras. Bull. bot. bras.
    Cat. Ci. Coll. Columb. Com. Contr. Cur. c. ca. cent. centr. cf. cit. coll. com.
    DC. Dept. Diam. Distr. depto. diam. distr. dtto.
    Encycl. Encyle. Est. Exot. e. ed. eg. e.g. ememd. ent. est.
    FIG. Fig. Figs. Fl. fig. figs. fl. flor. flumin. frag.
    Gard. Gen. Geo. g. gard. geograph.
    Herb. Hist. Hort. hb. hist.
    Ind. Is. illeg. infra. is.
    Jahrb. Jard. Jr. jug.
    Lab. Lam. Leg. Legum. Linn. lam. lat. leg. lin. loc. long.
    Mag. Mem. Mim. Mex. Mts. Mun. Mus. Nac. mem. mens. monac. mont. mun.
    Nat. Natl. Neg. No. nat. no. nom. nud.
    Ocas.
    PI. PL. Pl. Proc. Prodr. Prov. Pt. Pto. Publ. p. photo. pi. pl. pr. prov.
    Rev. reg. revis.
    ST. Sa. Sci. Soc. Sr. St. Sta. Sto. Sul. Suppl. Syst.
    s. sci. stat. stk. str. superfl. suppl. surv. syn.
    Tex. Trans t. tab. telegr.
    U.S. US. Univ.
    Veg. veg.
    Wm.
    I. II. III. IV. IX. V. VI. VII. VIII. X. XI. XII. XIII. XIV. XIX. XV. XVI. XVII.
    XVIII. XX. XXI. XXII. XXIII. XXIV. XXV.
    i. ii. iii. iv. ix. v. vi. vii. viii. x. xi. xii. xiii. xiv. xix. xv. xvi. xvii.
    xviii. xx. xxi. xxii. xxiii. xxiv. xxv.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

TOKENIZER = "mimosa.custom_tokenizer.v1"


def setup_tokenizer(nlp):
    not_letter = re.compile(r"[^a-zA-Z.']")
    removes = [{"pattern": s} for s in nlp.tokenizer.rules if not_letter.search(s)]
    tokenizer_util.remove_special_case(nlp, removes)
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, ABBREVS)


@registry.callbacks(TOKENIZER)
def make_customized_tokenizer():
    def customized_tokenizer(nlp):
        setup_tokenizer(nlp)

    return customized_tokenizer
