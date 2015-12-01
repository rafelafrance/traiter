import csv
import re
# import sys
from collections import namedtuple
# from pprint import pprint

# File names
base_name = 'vntraits110715'
in_name = base_name + '.csv'
out_name = base_name + '_01_sex.csv'

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


# Valid sex labels -- Only used in "sex=?" pattern
# valid_sex = dict(unknown=1, undetermined=1, uncertain=1,
#                 male=1, m=1, female=1, f=1)


def get_sex(field):
    # Examples: "sex=?", "sex: ?", etc.
    match = re.search(r' \b sex \b \W* (\w+)',
                      field, re.IGNORECASE | re.VERBOSE)
    if match:
        return match.group(1).lower()

    # Looking for "male" or "female" directly
    match = re.findall(r'\b (?: male | female ) s? \b',
                       field, re.IGNORECASE | re.VERBOSE)
    if match:
        # If we find conflicting matches then leave it alone
        sex = match[0].lower()
        for another_sex in match:
            another_sex = another_sex.lower()
            if another_sex != sex:
                return None

        # Everything matches so return it
        return sex

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

            # Default to value in the "sex" column
            dwc_sex = row.sex
            dwc_sex_source = 'sex'

            # If not found then look in "dynamicproperties"
            if not dwc_sex:
                dwc_sex_source = 'dynamicproperties'
                dwc_sex = get_sex(row.dynamicproperties)

            # If not found then look in "occurrenceremarks"
            if not dwc_sex:
                dwc_sex_source = 'occurrenceremarks'
                dwc_sex = get_sex(row.occurrenceremarks)

            # If not found then look in "fieldnotes"
            if not dwc_sex:
                dwc_sex_source = 'fieldnotes'
                dwc_sex = get_sex(row.fieldnotes)

            # Did we find anything?
            if dwc_sex:
                row = row._replace(dwc_sex=dwc_sex,
                                   dwc_sex_source=dwc_sex_source)
            else:
                dwc_sex_source = ''

            # Output to new CSV file
            print row.row_num, dwc_sex_source, dwc_sex
            writer.writerow(row)


if __name__ == '__main__':
    main()
