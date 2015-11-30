import csv
import re
# import sys
from collections import namedtuple
# from pprint import pprint

base_name = 'vntraits110715'
in_name = base_name + '.csv'
out_name = base_name + '_01_sex.csv'

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


sex_alias = dict(
        unknown='unknown', undetermined='unknown', uncertain='unknown',
        male='male', m='male', female='female', f='female')


def get_sex(field):
    match = re.search(r'\bsex\b\W*(\w+)', field)
    if match:
        sex = match.group(1).lower()
        if sex in sex_alias:
            return sex_alias[sex]
    match = re.findall(r'\b(?:male|female)\b', field)
    if match:
        for sex in match:
            if sex != match[0]:
                return None
        return match[0]
    return None


def main():
    with open(in_name, 'rb') as in_file, open(out_name, 'wb') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        row = reader.next()   # Header row
        writer.writerow(row)
        for raw_row in reader:
            row = Row._make(raw_row)
            dwc_sex_source = 'sex'
            dwc_sex = row.sex
            if not dwc_sex:
                dwc_sex_source = 'dynamicproperties'
                dwc_sex = get_sex(row.dynamicproperties)
            if not dwc_sex:
                dwc_sex_source = 'occurrenceremarks'
                dwc_sex = get_sex(row.occurrenceremarks)
            if not dwc_sex:
                dwc_sex_source = 'fieldnotes'
                dwc_sex = get_sex(row.fieldnotes)
            if dwc_sex:
                row = row._replace(dwc_sex=dwc_sex,
                                   dwc_sex_source=dwc_sex_source)
            print row.row_num, dwc_sex
            writer.writerow(row)


if __name__ == '__main__':
    main()
