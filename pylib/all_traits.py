"""All of the trait_builders."""

from pylib.trait_builders.body_mass_trait_builder import \
    BodyMassTraitBuilder
from pylib.trait_builders.ear_length_trait_builder import \
    EarLengthTraitBuilder
from pylib.trait_builders.embryo_count_trait_builder import \
    EmbryoCountTraitBuilder
from pylib.trait_builders.embryo_length_trait_builder import \
    EmbryoLengthTraitBuilder
from pylib.trait_builders.hind_foot_length_trait_builder import \
    HindFootLengthTraitBuilder
from pylib.trait_builders.lactation_state_trait_builder import \
    LactationStateTraitBuilder
from pylib.trait_builders.life_stage_trait_builder import \
    LifeStageTraitBuilder
from pylib.trait_builders.nipple_count_trait_builder import \
    NippleCountTraitBuilder
from pylib.trait_builders.nipple_state_trait_builder import  \
    NippleStateTraitBuilder
from pylib.trait_builders.ovaries_size_trait_builder import \
    OvariesSizeTraitBuilder
from pylib.trait_builders.ovaries_state_trait_builder import \
    OvariesStateTraitBuilder
from pylib.trait_builders.placental_scar_count_trait_builder import \
    PlacentalScarCountTraitBuilder
from pylib.trait_builders.pregnancy_state_trait_builder import \
    PregnancyStateTraitBuilder
from pylib.trait_builders.sex_trait_builder import \
    SexTraitBuilder
from pylib.trait_builders.tail_length_trait_builder import \
    TailLengthTraitBuilder
from pylib.trait_builders.testes_size_trait_builder import \
    TestesSizeTraitBuilder
from pylib.trait_builders.testes_state_trait_builder import \
    TestesStateTraitBuilder
from pylib.trait_builders.total_length_trait_builder import \
    TotalLengthTraitBuilder


TRAITS = {
    'body_mass': BodyMassTraitBuilder,
    'ear_length': EarLengthTraitBuilder,
    'embryo_count': EmbryoCountTraitBuilder,
    'embryo_length': EmbryoLengthTraitBuilder,
    'hind_foot_length': HindFootLengthTraitBuilder,
    'lactation_state': LactationStateTraitBuilder,
    'life_stage': LifeStageTraitBuilder,
    'nipple_count': NippleCountTraitBuilder,
    'nipple_state': NippleStateTraitBuilder,
    'ovaries_size': OvariesSizeTraitBuilder,
    'ovaries_state': OvariesStateTraitBuilder,
    'placental_scar_count': PlacentalScarCountTraitBuilder,
    'pregnancy_state': PregnancyStateTraitBuilder,
    'sex': SexTraitBuilder,
    'tail_length': TailLengthTraitBuilder,
    'testes_size': TestesSizeTraitBuilder,
    'testes_state': TestesStateTraitBuilder,
    'total_length': TotalLengthTraitBuilder,
}
