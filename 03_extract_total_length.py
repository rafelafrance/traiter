import csv
import re
import sys
from collections import namedtuple
from pprint import pprint

base_name = 'vntraits110715'
in_name = base_name + '_02_life_stage.csv'
out_name = base_name + '_03_total_length.csv'

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

measurements = re.compile(
    (r'\b (measurements) \b \D+ (\d+(?:\.\d*)?)([=/-]\d+)* \s* (g)?'),
    (re.IGNORECASE | re.VERBOSE))


def get_total_length(field):
    match = re.search(r'(?: \b t\.?l\.? \b | total \s* length )',
                      field, re.IGNORECASE | re.VERBOSE)
    if not match:
        return None

    match = re.search(r'\b totalLengthInMM \b \D+ (\d+(?:\.\d*)?)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units='mm')

    match = re.search(r' \b t\.?l\.? \b \D* (\d+(?:\.\d*)?) \s* ([a-z]*)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r' (\d+(?:\.\d*)?) \s* ([a-z]*) '
                      r' (?:\s* [a-z]*)? \D* \b t\.?l\.? \b',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r' \b [t]? total \s* length \D* '
                      r'(\d+(?:\.\d*)?) \s* ([a-z]*)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    match = re.search(r' \b total \s* length (?: \s* \D+ | $)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return None

    match = re.search(r' \b t \.? l [.;]? \s* \D+ ',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return None

    match = re.search(r't \.? l [.;:=i)]* $',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
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
                quantity = get_total_length(row.dynamicproperties)
            if not quantity:
                source = 'occurrenceremarks'
                quantity = get_total_length(row.occurrenceremarks)
            if not quantity:
                source = 'fieldnotes'
                quantity = get_total_length(row.fieldnotes)
            if quantity:
                row = row._replace(vto_bodyLength=quantity.value,
                                   vto_bodyLength_units=quantity.units,
                                   vto_bodyLength_source=source)
            print row.row_num, row.vto_bodyLength, row.vto_bodyLength_units
            writer.writerow(row)


if __name__ == '__main__':
    main()
