# use this like so: python words.py | sort | uniq > words.txt

import csv
import re
from collections import namedtuple

base_name = 'vntraits110715'
in_name = base_name + '_03_total_length.csv'

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


def main():
    with open(in_name, 'rb') as in_file:
        reader = csv.reader(in_file)
        row = reader.next()   # Header row
        for raw_row in reader:
            row = Row._make(raw_row)
            words = re.split(r'\W+', row.dynamicproperties)
            for word in words:
                word = word.lower()
                if word and not re.search(r'\d', word):
                    print word


if __name__ == '__main__':
    main()
