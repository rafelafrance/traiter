from dataclasses import dataclass
from typing import Callable

from .. import tokenizer
from ..patterns import colors
from ..patterns import dates
from ..patterns import elevations
from ..patterns import habitats
from ..patterns import lat_longs
from .base import BasePipelineBuilder


@dataclass
class Pipe:
    func: Callable
    kwargs: dict


class PipelineBuilder(BasePipelineBuilder):
    def tokenizer(self):
        tokenizer.setup_tokenizer(self.nlp)

    def colors(self, **kwargs) -> str:
        return self.add_traits([colors.COLORS], name="colors", **kwargs)

    def dates(self, **kwargs) -> str:
        return self.add_traits(
            [dates.DATES, dates.MISSING_DAYS], name="dates", **kwargs
        )

    def elevations(self, **kwargs) -> str:
        return self.add_traits(
            [elevations.ELEVATIONS, elevations.ELEVATION_RANGES],
            name="elevations",
            **kwargs,
        )

    def habitats(self, **kwargs) -> str:
        return self.add_traits(
            [habitats.HABITATS, habitats.NOT_HABITATS], name="habitats", **kwargs
        )

    def lat_longs(self, **kwargs) -> str:
        prev = self.add_traits(
            [lat_longs.LAT_LONGS], name="lat_longs", merge=True, **kwargs
        )
        return self.add_traits(
            [lat_longs.LAT_LONG_UNCERTAIN],
            name="lat_long_uncertain",
            after=prev,
        )
