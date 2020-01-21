"""All of the parsers."""

from traiter_vertnet.parsers import BODY_MASS
from traiter_vertnet.parsers import EAR_LENGTH
from traiter_vertnet.parsers.embryo_count import EMBRYO_COUNT
from traiter_vertnet.parsers import EMBRYO_LENGTH
from traiter_vertnet.parsers import HIND_FOOT_LENGTH
from traiter_vertnet.parsers import LACTATION_STATE
from traiter_vertnet.parsers.life_stage import LIFE_STAGE
from traiter_vertnet.parsers import NIPPLE_COUNT
from traiter_vertnet.parsers import NIPPLE_STATE
from traiter_vertnet.parsers import OVARY_SIZE
from traiter_vertnet.parsers import OVARIES_STATE
from traiter_vertnet.parsers import PLACENTAL_SCAR_COUNT
from traiter_vertnet.parsers import PREGNANCY_STATE
from traiter_vertnet.parsers import SEX
from traiter_vertnet.parsers import TAIL_LENGTH
from traiter_vertnet.parsers import TESTES_SIZE
from traiter_vertnet.parsers import TESTES_STATE
from traiter_vertnet.parsers import TOTAL_LENGTH

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
