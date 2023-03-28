from ..term_list import TermList

ADMIN_UNIT_TERMS = TermList().shared("us_locations").drop("county_label")

TERMS = TermList().shared("colors").add_trailing_dash()
TERMS.shared("elevations habitats lat_long numerics months units_length")
