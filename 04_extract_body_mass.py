import csv
import re
import sys
from collections import namedtuple
from pprint import pprint

base_name = 'vntraits110715'
in_name = base_name + '_03_total_length.csv'
out_name = base_name + '_04_body_mass.csv'

Row = namedtuple(
    'Row',
    ('row_num occurrenceid institutionid collectionid datasetid '
     'institutioncode collectioncode catalognumber '
     'scientificname class_ individualcount sex lifestage '
     'dynamicproperties occurrenceremarks fieldnotes '
     'dwc_sex dwc_sex_source '
     'dwc_lifeStage dwc_lifeStage_source '
     'vto_bodyLength vto_bodyLength_units vto_bodyLength_source '
     'vto_bodyMass vto_bodyMass_units vto_bodyMass_source'))

Quantity = namedtuple('Quantity', 'value units')


def get_body_mass(field):
    if not field:
        return None

    match = re.search(r'\b weightInGrams \b \D+ (\d+(?:\.\d*)?)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units='g')

    match = re.search(r'\b mass \s* in \s* grams \b \D+ (\d+(?:\.\d*)?)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units='g')

    match = re.search(r'\b measurements \b \D+ \d+ (?: - \d+ )+'
                      r'= (\d+(?:\.\d*)?) \s* ([a-z]*)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r' \b (?: body \s* mass | weight | wt ) \D* '
                      r'(\d+(?:\.\d*)?) \s* ([a-z]*)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r'(\d+(?:\.\d*)?) \s* \b '
                      r'( lb | pound | oz | ounce | ton '
                      r'| g  | gr | gram | kilogram | kg | kilo '
                      r'| mg ) s? \b',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r'\b measurements \b \D+ (:?\d+(?:\.\d*)?) (?: - \d+ )+'
                      r'(?: = [?])?',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return None

    match = re.search(r'\b (?: lb | pound | oz | ounce | ton '
                      r'| g  | gr | gram | kilogram | kg | kilo '
                      r'| mg ) s? \b',
                      field, re.IGNORECASE | re.VERBOSE)
    if not match:
        return None

    if re.search(r'\b (:? ounces | oz | gr? | mg | lbs? | grams? )'
                 r'\b ( \D+ | $ )',
                 field, re.IGNORECASE | re.VERBOSE):
        return None

    pprint(field)
    sys.exit()
    return None


def main():
    with open(in_name, 'rb') as in_file, open(out_name, 'wb') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        row = reader.next()   # Header row
        writer.writerow(row)
        for raw_row in reader:
            row = Row._make(raw_row)
            quantity = None
            source = None
            if not quantity:
                source = 'dynamicproperties'
                quantity = get_body_mass(row.dynamicproperties)
            if not quantity:
                source = 'occurrenceremarks'
                quantity = get_body_mass(row.occurrenceremarks)
            if not quantity:
                source = 'fieldnotes'
                quantity = get_body_mass(row.fieldnotes)
            if quantity:
                row = row._replace(vto_bodyMass=quantity.value,
                                   vto_bodyMass_units=quantity.units.lower(),
                                   vto_bodyMass_source=source)
            print row.row_num, row.vto_bodyMass, row.vto_bodyMass_units
            writer.writerow(row)


if __name__ == '__main__':
    main()
