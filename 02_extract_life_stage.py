import csv
import re
# import sys
from collections import namedtuple
# from pprint import pprint

# File names
base_name = 'vntraits110715'
in_name = base_name + '_01_sex.csv'
out_name = base_name + '_02_life_stage.csv'

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


# This dictionary is used to skip pattern matches that are not life stages
# lifeStage_junk = {
#     'is': 1, 'remarks': 1, 'found': 1, 'body': 1,
#     'es': 1, 'of': 1, 'must': 1, 'to': 1, 'd': 1}


def get_life_stage(field):
    # Example: life stage ?
    match = re.search(r' life \s* stage \W* ( \w+ )',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return match.group(1)

    # Examples: age ? | age class ?
    match = re.search(r' age (?: \s* class )? \W* ( \w+ )',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return match.group(1)

    # Examples:
    #   first ?  | second ? | etc.
    #   after first ? | after hatching ? | etc.
    match = re.search(
        (r' (?: after \s+ )?'
         r' (?: first | second | third | fourth | hatching ) \s+ ( \w+ )'),
        field, re.IGNORECASE | re.VERBOSE)
    if match:
        return match.group(0)

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

            # Default to value in the "lifestage" column
            dwc_lifeStage = row.lifestage
            dwc_lifeStage_source = 'lifestage'

            # If not found then look in "dynamicproperties"
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'dynamicproperties'
                dwc_lifeStage = get_life_stage(row.dynamicproperties)

            # If not found then look in "occurrenceremarks"
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'occurrenceremarks'
                dwc_lifeStage = get_life_stage(row.occurrenceremarks)

            # If not found then look in "fieldnotes"
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'fieldnotes'
                dwc_lifeStage = get_life_stage(row.fieldnotes)

            # Did we find anything?
            if dwc_lifeStage:
                row = row._replace(dwc_lifeStage=dwc_lifeStage,
                                   dwc_lifeStage_source=dwc_lifeStage_source)
            else:
                dwc_lifeStage_source = ''

            # Output to new CSV file
            print row.row_num, dwc_lifeStage_source, dwc_lifeStage
            writer.writerow(row)


if __name__ == '__main__':
    main()
