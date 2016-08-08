#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The line above is to signify that the script contains utf-8 encoded characters.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://github.com/rafelafrance/traiter
# Adapted from https://github.com/VertNet/dwc-indexer

__author__ = "John Wieczorek"
__contributors__ = "Raphael LaFrance, Aaron Steele, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "csv_sampler.py 2016-08-08T13:40+02:00"

import csv
import argparse
from vn_utils import tsv_dialect
from vn_utils import read_header

# need to install regex for the trait parsers to be used
# pip install regex

class CSVSampleProcessor:

    def __init__(self):
        pass

    def sample_csv_file(self, infilename, outfilename, header=None, nthrecord = 1000):
        # fields from the original harvest files
        dialect = tsv_dialect()
        csvheader = read_header(infilename)
        i = 0
        with open(outfilename, 'w') as outfile:
            writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=csvheader)
            with open(infilename, 'r') as infile:
                reader = csv.DictReader(infile, dialect=dialect, fieldnames=csvheader)
                for row in reader:
#                        print 'row: %s' % row
                    if i % nthrecord == 0:
                        writer.writerow(row)
                    i += 1

def _getoptions():
    """Parse command line options and return them."""
    parser = argparse.ArgumentParser()

    help = 'full path to the input file (required)'
    parser.add_argument("-i", "--inputfile", help=help)

    help = 'output file name, no path (required)'
    parser.add_argument("-o", "--outputfile", help=help)

    help = 'elect header inclusion (default = noheader)'
    parser.add_argument("-e", "--includeheader", help=help)

    help = 'select every nth record (default = 1000)'
    parser.add_argument("-n", "--nthrecord", help=help)

    help = 'log level (e.g., DEBUG, WARNING, INFO) (optional)'
    parser.add_argument("-l", "--loglevel", help=help)

    return parser.parse_args()

def main():
    options = _getoptions()

#    print 'options: %s' % options

    if options.inputfile is None or len(options.inputfile)==0 or \
       options.outputfile is None or len(options.outputfile)==0:
        s =  'syntax:\n'
        s += 'python csv_sampler.py'
        s += ' -i data/test_trait_fields.txt'
        s += ' -o outfile.txt'
        s += ' -n 1000'
        s += ' -e header'
        s += ' -l DEBUG'
        print '%s' % s
        return

    processor = CSVSampleProcessor()
    inputfile = options.inputfile
    outputfile = options.outputfile
    includeheader = options.includeheader
    nthrecord = int(options.nthrecord)
    loglevel = options.loglevel

    processor.sample_csv_file(inputfile, outputfile, includeheader, nthrecord)

if __name__ == '__main__':
    main()
