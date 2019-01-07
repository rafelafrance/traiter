"""Unit conversions."""


def convert(value, units):
    """Normalize the units to millimeters or grams."""
    units = units if units else ''
    factor = UNITS.get(units.lower(), '')
    if isinstance(value, list):
        value = [round(v * factor, 2) for v in value]
    else:
        value *= factor
        value = round(value, 2)
    return value


UNITS = {
    # No units given
    None: 1.0,
    '': 1.0,

    # Length
    'c.m.': 10.0,
    'centimeters': 10.0,
    'cm': 10.0,
    'cm.': 10.0,
    'cm.s': 10.0,
    'cms': 10.0,
    'feet': 304.8,
    'foot': 304.8,
    'ft': 304.8,
    'ft.': 304.8,
    'in': 25.4,
    'in.': 25.4,
    'inch': 25.4,
    'inches': 25.4,
    'ins': 25.4,
    'm.m': 1.0,
    'm.m.': 1.0,
    'meter': 1000.0,
    'meters': 1000.0,
    'millimeter': 1.0,
    'millimeters': 1.0,
    'mm': 1.0,
    'mm.': 1.0,
    'mm.s': 1.0,
    'mms': 1.0,

    # Mass
    'g': 1.0,
    'g.': 1.0,
    'gm': 1.0,
    'gm.': 1.0,
    'gms': 1.0,
    'gms.': 1.0,
    'gr': 1.0,
    'gr.': 1.0,
    'gram': 1.0,
    'grams': 1.0,
    'grs': 1.0,
    'kg': 1000.0,
    'kg.': 1000.0,
    'kgs': 1000.0,
    'kgs.': 1000.0,
    'kilograms': 1000.0,
    'lb': 453.593,
    'lb.': 453.593,
    'lbs': 453.593,
    'lbs.': 453.593,
    'mg': 0.001,
    'mg.': 0.001,
    'mgs.': 0.001,
    'mgs': 0.001,
    'ounce': 28.349,
    'ounces': 28.349,
    'oz': 28.349,
    'oz.': 28.349,
    'ozs': 28.349,
    'ozs.': 28.349,
    'pound': 453.593,
    'pounds': 453.593,
    'weightingrams': 1.0,
    'massingrams': 1.0,
}
