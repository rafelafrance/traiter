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
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "bigquery_loader.py 2016-09-01T11:49+02:00"

from googleapis import CloudStorage as CS
import csv
#from datetime import datetime

def remove_GCS_files(cs, filelist):
    '''
       Remove a list of files from GCS, where the filenames in the list are the paths
       within the bucket defined in cs
       (e.g., processed/YPM/9643f840-f762-11e1-a439-00145eb45e9a/2016-07-16-aa)
    '''
    n = 0
    for file in filelist:
        try:
            cs.delete_object(file)
            n += 1
            if n%100 == 0:
                print '%s files removed' % n
        except Exception, e:
            print 'Failed to remove file %s Exception: %s' % (file, e)
    return n

def get_file_list(inputfile):
    if inputfile is None or len(inputfile.strip())==0:
        print 'No file containing list of files given.'
        return None
    filelist = []
    with open(inputfile, 'rU') as data:
        reader = csv.DictReader(data, fieldnames=['gcspath'])
        for row in reader:
            file = row['gcspath'].split('/')[3]
            if file is not None and len(file.strip())>0:
                filelist.append(file)
                print '%s' % file
    return filelist

def main():
    ''' 
    Get the files to process from ./GCSFilesToDelete.txt
    Invoke without parameters as:
       python GCS_cleaner.py
    '''
    # Create a CloudStorage Manager to be able to access Google Cloud Storage based on
    # the downloads bucket.
    cs_cred = { "bucket_name": "vn-downloads2" }

    cs = CS.CloudStorage(cs_cred)

    # A list of candidate files can be found by 
    #   gsutil ls -l gs://vn-downloads2 > GCSFilesToDelete.txt
    # then filter for those before 60 days ago.
    
    filelist = get_file_list('GCSFilesToDelete.txt')
 
    filesremoved = remove_GCS_files(cs, filelist)

#    print '%s file(s) removed' % filesremoved
    
if __name__ == "__main__":
    main()