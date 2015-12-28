# python normalize.py data/vntraits110715.csv data/vntraits110715_norm.csv

import csv
import sys
import json
import regex
from pprint import pprint
from collections import namedtuple

LEN_KEY = {
    '_english_'                   : 'total length',
    '_shorthand_'                 : 'total length',
    'body'                        : 'head-body length',
    'Body'                        : 'head-body length',
    'BODY LENGTH'                 : 'head-body length',
    'Body Length'                 : 'head-body length',
    'body length'                 : 'head-body length',
    'Body length'                 : 'head-body length',
    'catalog'                     : 'total length',
    'Forklength'                  : 'fork length',
    'Fork length'                 : 'fork length',
    'fork length'                 : 'fork length',
    'headBodyLengthInMillimeters' : 'head-body length',
    'Length'                      : 'total length',
    'LENGTH'                      : 'total length',
    'length'                      : 'total length',
    'lengthInMillimeters'         : 'total length',
    'Lengths'                     : 'total length',
    'lengths'                     : 'total length',
    'max length'                  : 'total length',
    'maxlength'                   : 'total length',
    'mean length'                 : 'total length',
    'meas.'                       : 'total length',
    'Meas'                        : 'total length',
    'Meas.'                       : 'total length',
    'meas'                        : 'total length',
    'Meas,'                       : 'total length',
    'Meas. H.B.'                  : 'head-body length',
    'Measurement'                 : 'total length',
    'measurement'                 : 'total length',
    'MEASUREMENTS'                : 'total length',
    'Measurements'                : 'total length',
    'measurements'                : 'total length',
    'Measurementsnt'              : 'total length',
    'Mesurements'                 : 'total length',
    'Snout-Vent Length'           : 'snout-vent length',
    'SNOUT-VENT LENGTH'           : 'snout-vent length',
    'snout-vent length'           : 'snout-vent length',
    'Snout-vent length'           : 'snout-vent length',
    'Snout vent length'           : 'snout-vent length',
    'Snout-Vent length'           : 'snout-vent length',
    'snoutVentLengthInMM'         : 'snout-vent length',
    'Snout vent lengths'          : 'snout-vent length',
    'specimen'                    : 'total length',
    'Specimen'                    : 'total length',
    'specimens'                   : 'total length',
    'Standard Length'             : 'standard length',
    'Standard length'             : 'standard length',
    'standard length'             : 'standard length',
    'SVL.'                        : 'snout-vent length',
    'SVL'                         : 'snout-vent length',
    'tag'                         : 'total length',
    'Tag'                         : 'total length',
    'TL_'                         : 'total length',
    'Tl'                          : 'total length',
    'TL.'                         : 'total length',
    'T.l.'                        : 'total length',
    'Tl.'                         : 'total length',
    'tl.'                         : 'total length',
    'TL'                          : 'total length',
    't.l.'                        : 'total length',
    'T.L'                         : 'total length',
    'tl'                          : 'total length',
    'T.L.'                        : 'total length',
    'Tol'                         : 'total length',
    'ToL'                         : 'total length',
    'TOL'                         : 'total length',
    'TOTAL'                       : 'total length',
    'total'                       : 'total length',
    'Total'                       : 'total length',
    'total  length'               : 'total length',
    'Totallength'                 : 'total length',
    'Total Length'                : 'total length',
    'Total length'                : 'total length',
    'totalLength'                 : 'total length',
    'total length'                : 'total length',
    'Total  length'               : 'total length',
    'TOTAL LENGTH'                : 'total length',
    'total length in mm'          : 'total length',
    'totalLengthInMM'             : 'total length',
    'total lengths'               : 'total length',
}

LEN_UNITS = {
    ''             : 1.0,
    'centimeters'  : 10.0,
    'C.M.'         : 10.0,
    'CM.'          : 10.0,
    'CM'           : 10.0,
    'cm.'          : 10.0,
    'cm'           : 10.0,
    'cm.S'         : 10.0,
    'cmS'          : 10.0,
    'feet'         : 304.8,
    'feet inches.' : [304.8, 25.4],
    'FEET INCHES.' : [304.8, 25.4],
    'feet inches'  : [304.8, 25.4],
    'ft'           : 304.8,
    'ft.'          : 304.8,
    'FT'           : 304.8,
    'ft. in'       : [304.8, 25.4],
    'FT IN.'       : [304.8, 25.4],
    'ft in'        : [304.8, 25.4],
    'ft in.'       : [304.8, 25.4],
    'ft. in.'      : [304.8, 25.4],
    'FT IN'        : [304.8, 25.4],
    'ft. inches'   : [304.8, 25.4],
    'In'           : 25.4,
    'in.'          : 25.4,
    'in'           : 25.4,
    'IN.'          : 25.4,
    'IN'           : 25.4,
    'INCHES'       : 25.4,
    'inches'       : 25.4,
    'ins'          : 25.4,
    'meter'        : 1000.0,
    'METERS'       : 1000.0,
    'meters'       : 1000.0,
    'Millimeters'  : 1.0,
    'm.m'          : 1.0,
    'M.M.'         : 1.0,
    'MM'           : 1.0,
    'm.m.'         : 1.0,
    'mm'           : 1.0,
    'MM.'          : 1.0,
    'mm.'          : 1.0,
    '_mm_'         : 1.0,
    'MM.S'         : 1.0,
    'mm.S'         : 1.0,
    'mmS'          : 1.0,
}

MASS_KEY = {
    '_shorthand_'                     : 'total weight',
    '_english_'                       : 'total weight',
    'Body'                            : 'total weight',
    'BODY'                            : 'total weight',
    'Body mass'                       : 'total weight',
    'body mass'                       : 'total weight',
    'Body Mass'                       : 'total weight',
    'body weight'                     : 'total weight',
    'catalog'                         : 'total weight',
    'dead. Wt'                        : 'total weight',
    'full.weight'                     : 'total weight',
    'Live weight'                     : 'total weight',
    'live weight'                     : 'total weight',
    'live wt'                         : 'total weight',
    'Live wt'                         : 'total weight',
    'live wt.'                        : 'total weight',
    'Live wt.'                        : 'total weight',
    'MASS'                            : 'total weight',
    'Mass'                            : 'total weight',
    'mass'                            : 'total weight',
    'massInGrams'                     : 'total weight',
    'Measurement'                     : 'total weight',
    'measurement'                     : 'total weight',
    'Measurements'                    : 'total weight',
    'MEASUREMENTS'                    : 'total weight',
    'measurements'                    : 'total weight',
    'measurements at time of prep'    : 'total weight',
    'Measurements in English'         : 'total weight',
    'MEASUREMENTS IN RED BOOK SAY'    : 'total weight',
    'Measurements read'               : 'total weight',
    'measurements written on NK page' : 'total weight',
    'observedweight'                  : 'total weight',
    'total'                           : 'total weight',
    'Total weight'                    : 'total weight',
    'total weight'                    : 'total weight',
    'Total wt.'                       : 'total weight',
    'total wt'                        : 'total weight',
    'WEIGHT'                          : 'total weight',
    'Weight'                          : 'total weight',
    'weight'                          : 'total weight',
    'weightInGrams'                   : 'total weight',
    'Weights'                         : 'total weight',
    'weights'                         : 'total weight',
    'WT'                              : 'total weight',
    'wt.'                             : 'total weight',
    'WT.'                             : 'total weight',
    'Wt.'                             : 'total weight',
    'Wt'                              : 'total weight',
    'wt'                              : 'total weight',
}

MASS_UNITS = {
    ''               : 1.0,
    'g.'             : 1.0,
    'G.'             : 1.0,
    'G'              : 1.0,
    'g'              : 1.0,
    'gm'             : 1.0,
    'GM'             : 1.0,
    'GM.'            : 1.0,
    'gm.'            : 1.0,
    'gms.'           : 1.0,
    'GMS'            : 1.0,
    'gms'            : 1.0,
    'Gr'             : 1.0,
    'Gr.'            : 1.0,
    'gr.'            : 1.0,
    'GR'             : 1.0,
    'GR.'            : 1.0,
    'gr'             : 1.0,
    'gram'           : 1.0,
    'grams'          : 1.0,
    'GRAMS'          : 1.0,
    'Grams'          : 1.0,
    'grs'            : 1.0,
    'KG.'            : 1000.0,
    'KG'             : 1000.0,
    'Kg.'            : 1000.0,
    'kg.'            : 1000.0,
    'Kg'             : 1000.0,
    'kg'             : 1000.0,
    'kgs.'           : 1000.0,
    'kgs'            : 1000.0,
    'kilograms'      : 1000.0,
    'LB'             : 453.593,
    'LB.'            : 453.593,
    'lb'             : 453.593,
    'lb.'            : 453.593,
    'LB OZ'          : [453.593, 28.349],
    'lb. oz.'        : [453.593, 28.349],
    'lb oz'          : [453.593, 28.349],
    'LB OZ.'         : [453.593, 28.349],
    'lb oz.'         : [453.593, 28.349],
    'lb. oz'         : [453.593, 28.349],
    'LBS.'           : 453.593,
    'lbs'            : 453.593,
    'Lbs'            : 453.593,
    'lbs.'           : 453.593,
    'LBS'            : 453.593,
    'lbs oz.'        : [453.593, 28.349],
    'lbs oz'         : [453.593, 28.349],
    'lbs. oz.'       : [453.593, 28.349],
    'lbs. oz'        : [453.593, 28.349],
    'lbs ozs'        : [453.593, 28.349],
    'mg.'            : 0.001,
    'mg'             : 0.001,
    'mgs.'           : 0.001,
    'ounce'          : 28.349,
    'ounces'         : 28.349,
    'OZ.'            : 28.349,
    'oz.'            : 28.349,
    'oz'             : 28.349,
    'Oz.'            : 28.349,
    'Ozs.'           : 28.349,
    'ozs'            : 28.349,
    'ozs.'           : 28.349,
    'pound ounces'   : [453.593, 28.349],
    'POUNDS'         : 453.593,
    'pounds'         : 453.593,
    'pounds ounces.' : [453.593, 28.349],
    'pounds ounces'  : [453.593, 28.349],
}


def to_number(value):
    value = regex.sub(r'[^\d\.]', '', value)
    return round(float(value), 3)


def normalize(in_file_name, out_file_name):
    with open(in_file_name, 'rb') as in_file, open(out_file_name, 'w') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        row = reader.next()   # Header row
        row.extend(['Length', 'Weight'])
        writer.writerow(row)

        for row in reader:
            print reader.line_num
            lengths = row[-4]
            weights = row[-3]
            norm_len = None
            norm_wt  = None

            if lengths:
                json_len = json.loads(lengths)
                norm_len = []
                for key, obj in json_len.iteritems():
                    if obj['key'] not in LEN_KEY:
                        continue
                    label = LEN_KEY[obj['key']]
                    if isinstance(obj['units'], list):
                        units  = ' '.join(obj['units'])
                        value  = to_number(obj['value'][0]) * LEN_UNITS[units][0]
                        value += to_number(obj['value'][1]) * LEN_UNITS[units][1]
                    elif regex.search(r'- | to',
                                      obj['value'],
                                      regex.IGNORECASE | regex.VERBOSE):
                        values = regex.split(r'- | to',
                                             obj['value'],
                                             flags=regex.IGNORECASE | regex.VERBOSE)
                        value = (to_number(values[0]) * LEN_UNITS[obj['units']],
                                 to_number(values[1]) * LEN_UNITS[obj['units']])
                    else:
                        value = to_number(obj['value']) * LEN_UNITS[obj['units']]
                    norm_len.append((label, value))

            if weights:
                json_wt = json.loads(weights)
                norm_wt = []
                for key, obj in json_wt.iteritems():
                    if obj['key'] not in MASS_KEY:
                        continue
                    label = MASS_KEY[obj['key']]
                    if isinstance(obj['units'], list):
                        units  = ' '.join(obj['units'])
                        value  = to_number(obj['value'][0]) * MASS_UNITS[units][0]
                        value += to_number(obj['value'][1]) * MASS_UNITS[units][1]
                    elif regex.search(r'- | to', obj['value'], regex.IGNORECASE | regex.VERBOSE):
                        values = regex.split(r'- | to',
                                             obj['value'],
                                             flags=regex.IGNORECASE | regex.VERBOSE)
                        value = (to_number(values[0]) * MASS_UNITS[obj['units']],
                                 to_number(values[1]) * MASS_UNITS[obj['units']])
                    else:
                        value = to_number(obj['value']) * MASS_UNITS[obj['units']]
                    norm_wt.append((label, value))

            row.extend([json.dumps(norm_len), json.dumps(norm_wt)])
            writer.writerow(row)


if __name__ == '__main__':
    in_file_name  = sys.argv[1]
    out_file_name = sys.argv[2]

    normalize(in_file_name, out_file_name)
