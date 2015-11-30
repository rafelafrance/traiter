import csv
import re
# import sys
from collections import namedtuple
# from pprint import pprint

base_name = 'vntraits110715'
in_name = base_name + '_01_sex.csv'
out_name = base_name + '_02_life_stage.csv'

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


lifeStage_alias = {
        'unknown': 'unknown', 'undetermined': 'unknown',
        'uncertain': 'unknown',
        'adult': 'adult', 'juvenile': 'juvenile', 'hatching': 'hatching',
        'subadult': 'subadult', 'immature': 'immature',
        'first year': 'first year', 'second year': 'second year',
        'third year': 'third year', 'fourth year': 'fourth year',
        'hatching year': 'hatching year',
        'after hatching year': 'after hatching year',
        'after first year': 'after first year',
        'after second year': 'after second year',
        'young': 'young', 'fledgling': 'fledgling',
        'chick': 'chick', 'nestling': 'nestling', 'larval': 'larval',
        'metamorph': 'metamorph', 'newborn': 'newborn', 'other': 'other',
        'neonate': 'neonate', 'fetus': 'fetus', 'pup': 'pup',
        'embryo': 'embryo',
        'is': None, 'remarks': None, 'found': None, 'body': None, 'es': None,
        'of': None, 'must': None, }


def get_life_stage(field):
    match = re.search(
        (r'(?:life\s*stage\b|age(?:\s*class))\W*'
         r'((?:(?:(?:after\s+)?'
         r'(?:first|second|third|fourth|hatching))\s+)?\w+)'),
        field,
        re.IGNORECASE | re.VERBOSE)
    if match:
        lifeStage = match.group(1).lower()
        if re.match(r'\d+$', lifeStage):
            return lifeStage
        if lifeStage in lifeStage_alias:
            return lifeStage_alias[lifeStage]
    return None


def main():
    with open(in_name, 'rb') as in_file, open(out_name, 'wb') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        row = reader.next()   # Header row
        writer.writerow(row)
        for raw_row in reader:
            row = Row._make(raw_row)
            dwc_lifeStage_source = 'lifestage'
            dwc_lifeStage = row.lifestage
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'dynamicproperties'
                dwc_lifeStage = get_life_stage(row.dynamicproperties)
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'occurrenceremarks'
                dwc_lifeStage = get_life_stage(row.occurrenceremarks)
            if not dwc_lifeStage:
                dwc_lifeStage_source = 'fieldnotes'
                dwc_lifeStage = get_life_stage(row.fieldnotes)
            if dwc_lifeStage:
                row = row._replace(dwc_lifeStage=dwc_lifeStage,
                                   dwc_lifeStage_source=dwc_lifeStage_source)
            print row.row_num, dwc_lifeStage
            writer.writerow(row)


if __name__ == '__main__':
    main()
