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
__version__ = "harvest_record_processor.py 2016-07-13T15:07+02:00"

import csv
import argparse
from field_utils import index_fields
from field_utils import HARVEST_FIELDS
from vn_utils import tsv_dialect
from vn_utils import record_level_resolution
from vn_utils import license_resolution
from vn_utils import dynamicproperties_resolution
from vn_utils import occurrence_resolution
from vn_utils import sex_resolution
from vn_utils import event_resolution
from vn_utils import location_resolution
from vn_utils import georef_resolution
from vn_utils import identification_resolution
from vn_utils import is_fossil
from vn_utils import is_mappable
from vn_utils import was_captive
from vn_utils import was_invasive
from vn_utils import has_media
from vn_utils import has_tissue
from vn_utils import has_typestatus
from vn_utils import vn_type
from vn_utils import rec_rank
from datetime import datetime
from trait_parsers.body_mass_parser import BodyMassParser
from trait_parsers.life_stage_parser import LifeStageParser
from trait_parsers.sex_parser import SexParser
from trait_parsers.total_length_parser import TotalLengthParser

# need to install regex for the trait parsers to be used
# pip install regex

INDEX_FIELDS = index_fields()

class VertHarvestFileProcessor:

    def __init__(self):
        self.body_mass_parser    = BodyMassParser()
        self.life_stage_parser   = LifeStageParser()
        self.sex_parser          = SexParser()
        self.total_length_parser = TotalLengthParser()

    def parse_row_for_traits(self, row):
        '''
        Parse traits out of the given fields in the row.
        '''
        strings = [row['dynamicproperties'], row['occurrenceremarks'], row['fieldnotes']]
        traits  = self.sex_parser.preferred_or_search(row['sex'], strings)
        traits.update(self.life_stage_parser.preferred_or_search(row['lifestage'], strings))

        # Only parse measurements if the record is not an observation. Expects 
        # row['vntype'] to have been determined.
        if row.has_key('vntype') and 'obs' in row['vntype'].lower():
            traits.update({'haslength': 0, 'lengthinmm': None, 'lengthunitsinferred': None})
            traits.update({'hasmass': 0, 'massing': None, 'massunitsinferred': None})
        else:
            traits.update(self.total_length_parser.search_and_normalize(strings))
            traits.update(self.body_mass_parser.search_and_normalize(strings))
 
#        print 'strings: %s\ntraits: %s' % (strings, traits)       
        return traits

    def parse_harvest_file(self, infilename, outfilename, header=None):
        # fields from the original harvest files
        dialect = tsv_dialect()

        with open(outfilename, 'w') as outfile:
            writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=INDEX_FIELDS)
            # A header is not used in VertNet indexing chunks. The field order must be 
            # defined in the indexer. A header can be added to the output file by setting 
            # the optional header parameter.
            if header.lower()=='header':
                writer.writeheader()

            with open(infilename, 'r') as infile:
                reader = csv.DictReader(infile, dialect=dialect, fieldnames=HARVEST_FIELDS)
                for row in reader:
#                    print 'row: %s' % row
                    newrow = self.process_harvest_row(row)
#                    print 'newrow: %s' % newrow
                    if newrow is not None:
                        wrong_fields = [k for k in newrow if k not in INDEX_FIELDS]
#                        print 'wrong fields: %s' % wrong_fields
                        for f in wrong_fields:
                            newrow.pop(f)
#                        print 'newrow: %s' % newrow
                        writer.writerow(newrow)
#                         try:
#                             writer.writerow(newrow)
#                         except:
#                             print 'Failed to write row:\n%s' % newrow

    def process_harvest_row(self, row):
        """Produces an output record ready for indexing based on a post-harvest input 
           record with structure determined by HARVEST_FIELDS. Adds new fields and 
           changes contents of some existing fields. All others remain as in the input.
        """
        
        ### ISFOSSIL ###
        row['isfossil'] = is_fossil(row) # must come before record_level_resolution

        ### RECORD_LEVEL ###
        # Create a record identifier (keyname) - docid in Google App Engine documents
        # Create a reference to the record details (references)
        # Other fields determined: keyname, references, citation, bibliographiccitation, 
        #   basisofrecord, dctype
        c = record_level_resolution(row)
#        print 'ids:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        # The record cannot be propagated without an identifier
        if row.has_key('keyname') == False or len(row['keyname']) == 0:
            return None

        ### VNTYPE ###
        row['vntype'] = vn_type(row) # must come before traits

        ### LICENSE ###
        # Translate the field 'iptlicense' to field 'license' if the latter is missing
        # fields determined: license, haslicense
        c = license_resolution(row)
#        print 'license:\n%s' % license
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### DYNAMICPROPERTIES ###
        # Process the dynamicProperties prior to trait extraction
        dp = dynamicproperties_resolution(row)
        if dp is not None and len(dp) > 0:
            row['dynamicproperties'] = dp

        ### WASCAPTIVE ###
        row['wascaptive'] = was_captive(row) # must come before occurrence_resolution

        ### OCCURRENCE ###
        # Fields determined: occurrenceremarks, establishmentmeans (relies on was_captive)
        c = occurrence_resolution(row)
#        print 'occurrence:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### EVENT ###
        # Fields determined: year, month, day, startdayofyear, enddayofyear, eventdate,
        #   eventremarks, verbatimeventdate
        c = event_resolution(row)
#        print 'event:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### LOCATION ###
        # Fields determined: localityremarks, locality
        c = location_resolution(row)
#        print 'location:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### GEOREFERENCE ###
        # Fields determined: decimallatitude, decimallongitude, geodeticdatum
        #   coordinateuncertaintyinmeters, georeferenceddate, georeferencesources
        c = georef_resolution(row)
#        print 'georef:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### IDENTIFICATION ###
        # Fields determined: previousidentifications, identificationreferences, 
        #    identificationremarks, dateidentified, typestatus, dateidentified
        c = identification_resolution(row)
#        print 'identification:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### TRAITS ###
        # Process the traits and add trait fields to the record, but only if the record
        # is not an observation. Requires vntype to have been determined.
        # Fields determined: haslength, haslifestage, hasmass, hassex, 
        #   lifestageverbatim, sexverbatim, lengthinmm, massing, 
        #   lengthunitsinferred, massunitsinferred
        traits = self.parse_row_for_traits(row)
#        print 'traits:\n%s' % traits
        for trait in traits:
            row[trait]=traits[trait]
        row['underivedsex'] = row['sex']
        row['underivedlifestage'] = row['lifestage']
        row['sex'] = row['derivedsex']
        row['lifestage'] = row['derivedlifestage']
        row.pop('derivedsex')
        row.pop('derivedlifestage')

        ### SEX ###
        # Standardize the field 'sex' after all trait extraction is done
        # fields determined: sex
        row['sex'] = sex_resolution(row['sex'])

        # VertNet-specific flags - post-precessing
        row['mappable'] = is_mappable(row) # must come after georef_resolution
        row['hasmedia'] = has_media(row)
        row['wasinvasive'] = was_invasive(row)
        row['hastissue'] = has_tissue(row)
        row['hastypestatus'] = has_typestatus(row)

        # The index has a default sort order. In VertNet we set it based on rank, which 
        # is a rough assessment of fitness for a variety of uses requiring a taxon at a 
        # georeferenced place and time. Must come after all other cleanup.
        row['rank'] = rec_rank(row)

        # hashid is a hash of the keyname as a means to evenly distribute records among bins
        # for parallel processing with bins having 10k or less records as recommended by 
        # Google engineers.
        row['hashid'] = hash(row['keyname'])%9999

        # Set numeric fields that are None to zero for indexing
#        numeric_field_list = ['coordinateuncertaintyinmeters', 'year', 'month', 'day', 
#            'startdayofyear', 'enddayofyear']
#        for f in numeric_field_list:
#            if row[f] is None:
#                row[f] = 0

        return row

def _getoptions():
    """Parse command line options and return them."""
    parser = argparse.ArgumentParser()

    help = 'full path to the input file (required)'
    parser.add_argument("-i", "--inputfile", help=help)

    help = 'output file name, no path (required)'
    parser.add_argument("-o", "--outputfile", help=help)

    help = 'elect header inclusion (default = noheader)'
    parser.add_argument("-e", "--includeheader", help=help)

    help = 'log level (e.g., DEBUG, WARNING, INFO) (optional)'
    parser.add_argument("-l", "--loglevel", help=help)

    return parser.parse_args()

def main():
    options = _getoptions()

#    print 'options: %s' % options

    if options.inputfile is None or len(options.inputfile)==0 or \
       options.outputfile is None or len(options.outputfile)==0:
        s =  'syntax:\n'
        s += 'python harvest_record_processor.py'
        s += ' -i testdata-aa-1record'
        s += ' -o outfile.txt'
        s += ' -e header'
        s += ' -l DEBUG'
        print '%s' % s
        return

    processor = VertHarvestFileProcessor()
    inputfile = options.inputfile
    outputfile = options.outputfile
    includeheader = options.includeheader
    loglevel = options.loglevel

    processor.parse_harvest_file(inputfile, outputfile, includeheader)

if __name__ == '__main__':
    main()
