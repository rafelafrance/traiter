"""All of the trait_builders."""

from lib.trait_builders.sex_trait_builder import SexTraitBuilder
from lib.trait_builders.body_mass_trait_builder import \
    BodyMassTraitBuilder
from lib.trait_builders.life_stage_trait_builder import \
    LifeStageTraitBuilder
from lib.trait_builders.ear_length_trait_builder import \
    EarLengthTraitBuilder
from lib.trait_builders.tail_length_trait_builder import \
    TailLengthTraitBuilder
from lib.trait_builders.testes_size_trait_builder import \
    TestesSizeTraitBuilder
from lib.trait_builders.testes_state_trait_builder import \
    TestesStateTraitBuilder
from lib.trait_builders.total_length_trait_builder import \
    TotalLengthTraitBuilder
from lib.trait_builders.hind_foot_length_trait_builder import \
    HindFootLengthTraitBuilder
from lib.trait_builders.ovaries_state_trait_builder import \
    OvariesStateTraitBuilder
from lib.trait_builders.ovaries_size_trait_builder import \
    OvariesSizeTraitBuilder


TRAITS = {
    'sex': SexTraitBuilder,
    'body_mass': BodyMassTraitBuilder,
    'life_stage': LifeStageTraitBuilder,
    'total_length': TotalLengthTraitBuilder,
    'tail_length': TailLengthTraitBuilder,
    'hind_foot_length': HindFootLengthTraitBuilder,
    'ear_length': EarLengthTraitBuilder,
    'testes_size': TestesSizeTraitBuilder,
    'testes_state': TestesStateTraitBuilder,
    'ovaries_size': OvariesSizeTraitBuilder,
    'ovaries_state': OvariesStateTraitBuilder,
}
