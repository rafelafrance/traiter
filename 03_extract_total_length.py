import csv
import re
import sys
from collections import namedtuple
from pprint import pprint

# File names
base_name = 'vntraits110715'
in_name = base_name + '_02_life_stage.csv'
out_name = base_name + '_03_total_length.csv'

# It's easier to use a named tuple to access CSV fields
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

# This named tuple is used to return multiple values from the regex search
Quantity = namedtuple('Quantity', 'value units')


def get_total_length(field):
    # match = re.search(r'(?: \b t\.?l\.? \b | total \s* length )',
    #                   field, re.IGNORECASE | re.VERBOSE)
    # if not match:
    #     return None

    # Example: totalLengthInMM: 99.9
    match = re.search(r'\b totalLengthInMM \b \D+ (\d+(?:\.\d*)?)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units='mm')

    # Examples: tl=9.9 mm | t.l. 9.9in
    match = re.search(r' \b t\.?l\.? \b \D* (\d+(?:\.\d*)?) \s* ([a-z]*)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    # Examples: 9.9 in t.l.  | 9.9 mm junk tl
    match = re.search(r' (\d+(?:\.\d*)?) \s* ([a-z]*) '
                      r' (?:\s* [a-z]*)? \D* \b t\.?l\.? \b',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    # Examples: total length: 9.9 cm  | totallength=99mm
    # Note: The extra [t]? handles some typos
    match = re.search(r' \b [t]? total \s* length \D* '
                      r' (\d+(?:\.\d*)?) \s* ([a-z]*) ',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return Quantity(match.group(1), units=match.group(2))

    # Skip: total length word
    if re.search(r' \b total \s* length (?: \s* \D+ | $)',
                 field, re.IGNORECASE | re.VERBOSE):
        return None

    # Skip: tl; word
    if re.search(r' \b t \.? l [.;:=i)]* (:? \s* \D+ | $ )',
                 field, re.IGNORECASE | re.VERBOSE):
        return None

    # Skip: measurements: 9.9g
    if re.search(r' \b measurements? \D+ (\d+(?:\.\d*)?) \s* g',
                 field, re.IGNORECASE | re.VERBOSE):
        return None

    # Skip: if missing TL or length or measurements
    if not re.search(r' (?: measurements? | t\.?l\.? | length)',
                     field, re.IGNORECASE | re.VERBOSE):
        return None

    pprint(field)
    sys.exit()
    return None


def main():
    with open(in_name, 'rb') as in_file, open(out_name, 'wb') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)

        # Handle the header row
        row = reader.next()
        writer.writerow(row)

        # Handle all data rows
        for raw_row in reader:
            row = Row._make(raw_row)

            # Try "dynamicproperties" first
            source = 'dynamicproperties'
            quantity = get_total_length(row.dynamicproperties)

            # If not found then look in "occurrenceremarks"
            if not quantity:
                source = 'occurrenceremarks'
                quantity = get_total_length(row.occurrenceremarks)

            # If not found then look in "fieldnotes"
            if not quantity:
                source = 'fieldnotes'
                quantity = get_total_length(row.fieldnotes)

            # Did we find anything?
            if quantity:
                row = row._replace(vto_bodyLength=quantity.value,
                                   vto_bodyLength_units=quantity.units,
                                   vto_bodyLength_source=source)
            else:
                source = ''

            # Output to new CSV file
            print row.row_num, source, row.vto_bodyLength, \
                row.vto_bodyLength_source
            writer.writerow(row)


if __name__ == '__main__':
    main()
