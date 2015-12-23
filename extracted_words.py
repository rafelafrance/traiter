# python extracted_words.py data/vntraits110715.csv autoextract_body_length key | sort | uniq > data/len_keys.txt

import csv
import sys
import json
import regex
from pprint import pprint
from collections import namedtuple
from collections import Counter


def get_headers(in_name):
    with open(in_name, 'rb') as in_file:
        reader = csv.reader(in_file)
        row = reader.next()   # Header row
    return row


def get_word_counts(Row, in_file_name, column_name, json_field):
    cnt = Counter()
    with open(in_file_name, 'rb') as in_file:
        reader = csv.reader(in_file)
        row = reader.next()   # Header row
        for lrow in reader:
            trow_ = Row._make(lrow)
            row   = trow_._asdict()
            cell  = row[column_name]
            if not cell:
                continue
            jcell = json.loads(cell)
            for key, obj in jcell.iteritems():
                if isinstance(obj[json_field], list):
                    word = ' '.join(obj[json_field])
                else:
                    word = obj[json_field]
                #print type(word)
                cnt[word] += 1
    return cnt


def print_counts(cnt):
    for key, n in cnt.iteritems():
        print key, n


if __name__ == '__main__':
    in_file_name = sys.argv[1]
    column_name = sys.argv[2]
    json_field = sys.argv[3]

    headers = get_headers(in_file_name)
    Row = namedtuple('Row', headers, rename=True)
    cnt = get_word_counts(Row, in_file_name, column_name, json_field)
    print_counts(cnt)
