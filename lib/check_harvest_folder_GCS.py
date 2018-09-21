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

# Adapted from https://github.com/VertNet/bigquery

__author__ = "John Wieczorek"
__contributors__ = "Javier Otegui, John Wieczorek"
__copyright__ = "Copyright 2018 vertnet.org"
__version__ = "check_harvest_folder_GCS.py 2018-09-21T12:50-03:00"

from googleapis import CloudStorage as CS
from google_creds import cs_cred
from harvest_utils import get_harvest_folders_from_file
import csv

def check_harvest_folder_GCS(cs, folders):
    '''
       Check that the harvest folders on the list coming out of Carto exist, and how
       many files are in each.
    '''
    if cs is None:
        print 'No Google Cloud Storage dispatcher given in %s.' % __version__
    if folders is None:
        print 'No folder to check in %s.' % __version__
    total = 0
    i = 0
    for f in folders:
        j = 0
        if f.has_key('harvestfolder') and len(f['harvestfolder'].strip()) > 0:
#            print 'harvest folder: %s' % f['harvestfolder']
            bucket = f['harvestfolder'].split('/', 1)[0]
            resource = f['harvestfolder'].split('/', 1)[1]

            # Make a list of files in the harvest folder
            uri_list = []
            if 'items' in cs.list_bucket(prefix=resource):
                for item in cs.list_bucket(prefix=resource)['items']:
                    uri = '/'.join(["gs:/", bucket, item['name']])
                    uri_list.append(uri)
                    j += 1
            else:
                # Fail unless all folders can be found. 
                s = 'Resource %s not found in %s. ' % (resource, bucket)
                s += 'Check harvestfoldernew value in Carto.'
                print '%s' % s
                return False
        i += 1
        total += j
        print '%s) %s files for %s %s %s' % (i, j, f['icode'], f['gbifdatasetid'], f['harvestfolder'])
    print 'Total shards: %s' % total
    return True

def main():
    ''' 
    Get the folders to process. Create the ./data/resource_staging.csv by exporting from
    Carto the results of the query (modified to filter on lastindexed, for example):
      SELECT icode,gbifdatasetid,harvestfolder 
      FROM resource_staging
      WHERE 
      lastindexed='2017-01-23'
      ORDER BY icode, gbifdatasetid ASC

    Invoke without parameters as:
       python check_harvest_folder_GCS.py
    '''
    inputfile = './data/resource_staging.csv'
    # Create a CloudStorage Manager to be able to access Google Cloud Storage based on
    # the credentials stored in cs_cred.
    cs = CS.CloudStorage(cs_cred)

    # Create a list of folders on Google Cloud Storage to process
    harvestfolders = get_harvest_folders_from_file(inputfile)

    if harvestfolders is None:
        return None

    # Do a preliminary check of the folders in the harvest list
    return check_harvest_folder_GCS(cs, harvestfolders)

if __name__ == "__main__":
    main()