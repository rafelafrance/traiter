"""All of the parsers."""

from pylib.vertnet.parsers.body_mass import BODY_MASS
from pylib.vertnet.parsers.ear_length import EAR_LENGTH
from pylib.vertnet.parsers.embryo_count import EMBRYO_COUNT
from pylib.vertnet.parsers.embryo_length import EMBRYO_LENGTH
from pylib.vertnet.parsers.hind_foot_length import HIND_FOOT_LENGTH
from pylib.vertnet.parsers.lactation_state import LACTATION_STATE
from pylib.vertnet.parsers.life_stage import LIFE_STAGE
from pylib.vertnet.parsers.nipple_count import NIPPLE_COUNT
from pylib.vertnet.parsers.nipple_state import NIPPLE_STATE
from pylib.vertnet.parsers.ovaries_size import OVARY_SIZE
from pylib.vertnet.parsers.ovaries_state import OVARIES_STATE
from pylib.vertnet.parsers.placental_scar_count import PLACENTAL_SCAR_COUNT
from pylib.vertnet.parsers.pregnancy_state import PREGNANCY_STATE
from pylib.vertnet.parsers.sex import SEX
from pylib.vertnet.parsers.tail_length import TAIL_LENGTH
from pylib.vertnet.parsers.testes_size import TESTES_SIZE
from pylib.vertnet.parsers.testes_state import TESTES_STATE
from pylib.vertnet.parsers.total_length import TOTAL_LENGTH

TRAITS = {
    'body_mass': BODY_MASS,
    'ear_length': EAR_LENGTH,
    'embryo_count': EMBRYO_COUNT,
    'embryo_length': EMBRYO_LENGTH,
    'hind_foot_length': HIND_FOOT_LENGTH,
    'lactation_state': LACTATION_STATE,
    'life_stage': LIFE_STAGE,
    'nipple_count': NIPPLE_COUNT,
    'nipple_state': NIPPLE_STATE,
    'ovaries_size': OVARY_SIZE,
    'ovaries_state': OVARIES_STATE,
    'placental_scar_count': PLACENTAL_SCAR_COUNT,
    'pregnancy_state': PREGNANCY_STATE,
    'sex': SEX,
    'tail_length': TAIL_LENGTH,
    'testes_size': TESTES_SIZE,
    'testes_state': TESTES_STATE,
    'total_length': TOTAL_LENGTH,
}
