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

# This file contains common utility functions for pulling a list of harvest folders
# out of a resrouce_staging export of the VertNet resource registry in CartoDB

__author__ = "John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "harvest_utils.py 2016-07-26T14:07+2:00"

from vn_utils import read_header
import csv

def get_harvest_folders_from_file(inputfile):     
    '''
       Create a list of folders on Google Cloud Storage to process. List comes from
       inputfile, which must contain the fields:
           icode, gbifdatasetid, harvestfoldernew
    '''
    harvestfolders = []
    fieldnames = ['icode', 'gbifdatasetid', 'harvestfolder']

    dialect = csv.excel
    
    header = read_header(inputfile, dialect)
#    print 'header: %s' % header
    if header is None:
        print 'Can not read header from %s.' % inputfile
        return None

    # Populate the list of folders to harvest from the inputfile    
    with open(inputfile, 'r') as infile:
        reader = csv.DictReader(infile, dialect=dialect, fieldnames=header)
        reader.next()
        for field in fieldnames:
           if field not in header:
               print 'Required field %s not found in %s.' % (field, inputfile)
               return None
        for row in reader:
            newrow = {}
#            print 'row: %s' % row
            for field in fieldnames:
                newrow[field]=row[field]
            harvestfolders.append(row)
    return harvestfolders