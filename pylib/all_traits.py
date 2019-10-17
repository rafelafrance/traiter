"""All of the parsers."""

from pylib.parsers.body_mass import BodyMass
from pylib.parsers.ear_length import EarLength
from pylib.parsers.embryo_count import EmbryoCount
from pylib.parsers.embryo_length import EmbryoLength
from pylib.parsers.hind_foot_length import HindFootLength
from pylib.parsers.lactation_state import LactationState
from pylib.parsers.life_stage import LifeStage
from pylib.parsers.nipple_count import NippleCount
from pylib.parsers.nipple_state import NippleState
from pylib.parsers.ovaries_size import OvariesSize
from pylib.parsers.ovaries_state import OvariesState
from pylib.parsers.placental_scar_count import PlacentalScarCount
from pylib.parsers.pregnancy_state import PregnancyState
from pylib.parsers.sex import Sex
from pylib.parsers.tail_length import TailLength
from pylib.parsers.testes_size import TestesSize
from pylib.parsers.testes_state import TestesState
from pylib.parsers.total_length import TotalLength

TRAITS = {
    'body_mass': BodyMass,
    'ear_length': EarLength,
    'embryo_count': EmbryoCount,
    'embryo_length': EmbryoLength,
    'hind_foot_length': HindFootLength,
    'lactation_state': LactationState,
    'life_stage': LifeStage,
    'nipple_count': NippleCount,
    'nipple_state': NippleState,
    'ovaries_size': OvariesSize,
    'ovaries_state': OvariesState,
    'placental_scar_count': PlacentalScarCount,
    'pregnancy_state': PregnancyState,
    'sex': Sex,
    'tail_length': TailLength,
    'testes_size': TestesSize,
    'testes_state': TestesState,
    'total_length': TotalLength,
}
