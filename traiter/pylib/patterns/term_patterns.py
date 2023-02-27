from ..terms.db import Db

COLOR_TERMS = Db.shared("colors")
COLOR_TERMS += Db.trailing_dash(COLOR_TERMS, label="color")
COLOR_REPLACE = COLOR_TERMS.pattern_dict("replace")
COLOR_REMOVE = COLOR_TERMS.pattern_dict("remove")

UNIT_TERMS = Db.shared("units")
UNIT_FACTORS = UNIT_TERMS.pattern_dict("factor")
UNIT_FACTORS = {k: float(v) for k, v in UNIT_FACTORS.items()}

TIME_TERMS = Db.shared("time")

NUMERIC_TERMS = Db.shared("numerics")
