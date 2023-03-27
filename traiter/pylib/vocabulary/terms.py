from ..term_list import TermList

ADMIN_UNIT_TERMS = TermList().shared("us_locations").drop("county_label")

TERMS = TermList().shared("colors").add_trailing_dash()
TERMS.shared("habitats labels lat_long numerics time units")
