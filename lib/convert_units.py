"""Normalize units to millimeters or grams."""


def convert(value, units):
    """Normalize either single units or a list of units."""
    units = units if units else ''
    factor = UNITS.get(units.lower(), 1.0)
    if isinstance(value, list):
        value = [round(v * factor, 2) for v in value]
    else:
        value *= factor
        value = round(value, 2)
    return value


UNITS = {
    # Length
    'c.m.': 10.0,
    'centimeters': 10.0,
    'cm': 10.0,
    'cm.': 10.0,
    'cm.s': 10.0,
    'cms': 10.0,
    "'": 304.8,
    'feet': 304.8,
    'foot': 304.8,
    'ft': 304.8,
    'ft.': 304.8,
    '"': 25.4,
    'in': 25.4,
    'in.': 25.4,
    'inch': 25.4,
    'inches': 25.4,
    'ins': 25.4,
    'meter': 1000.0,
    'meters': 1000.0,

    # Mass
    'kg': 1000.0,
    'kg.': 1000.0,
    'kgs': 1000.0,
    'kgs.': 1000.0,
    'kilograms': 1000.0,
    'lb': 453.5924,
    'lb.': 453.5924,
    'lbs': 453.5924,
    'lbs.': 453.5924,
    'mg': 0.001,
    'mg.': 0.001,
    'mgs.': 0.001,
    'mgs': 0.001,
    'ounce': 28.34952,
    'ounces': 28.34952,
    'oz': 28.34952,
    'oz.': 28.34952,
    'ozs': 28.34952,
    'ozs.': 28.34952,
    'pound': 453.5924,
    'pounds': 453.5924,
}
