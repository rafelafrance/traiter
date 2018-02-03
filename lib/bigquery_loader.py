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
__copyright__ = "Copyright 2017 vertnet.org"
__version__ = "bigquery_loader.py 2017-11-30T14:33-03:00"

from googleapis import CloudStorage as CS
from googleapis import BigQuery as BQ
from creds.google_creds import cs_cred
from creds.google_creds import bq_cred
from field_utils import index_fields
from datetime import datetime
import time

def remove_GCS_files(cs, filelist):
    '''
       Remove a list of files from GCS, where the filenames in the list are the paths
       within the bucket defined in cs
       (e.g., processed/YPM/9643f840-f762-11e1-a439-00145eb45e9a/2016-07-16-aa)
    '''
    for file in filelist:
        try:
            cs.delete_object(file)
        except Exception, e:
            print 'Failed to remove file %s Exception: %s' % (file, e)

def get_processed_files(cs, folder):
    '''
       Get the list of files in a folder of processed files.
    '''
    bucket = 'vertnet-harvesting'
    resource = 'processed'
    filecount = 0
    folderlist = {}
    listing = []
    dataset = '%s/%s' % (resource, folder)
    bucketlist = cs.list_bucket(prefix=resource+'/'+folder+'/')
    if 'items' in bucketlist:
        for item in bucketlist['items']:
            uri = '/'.join(["gs:/", bucket, item['name']])
            listing.append(uri)
            filecount += 1
    folderlist[dataset] = { 'dataset': dataset, 'listing': listing }
    return folderlist

def get_all_processed_folders(cs):
    '''
       Get the list of folders of processed files to copy into BigQuery.
    '''
    bucket = 'vertnet-harvesting'
    resource = 'processed'
    foldercount = 0
    filecount = 0
    token = None
    # Make a list of folders in the processed folder
    datasetlist = []
    folderlist = {}
    uri_list = []
    thereismore = True
    while filecount==0 or token is not None:
        bucketlist = cs.list_bucket(prefix=resource, pageToken=token)
        if 'items' in bucketlist:
            for item in bucketlist['items']:
                uri = '/'.join(["gs:/", bucket, item['name']])
                parts = item['name'].split('/')
                if len(parts) == 4:
                    dataset = '/'.join([parts[0],parts[1],parts[2]])
                    if dataset not in datasetlist:
                        datasetlist.append(dataset)
                        foldercount += 1
                        listing = []
                        listing.append(uri)
                        folderlist[dataset] = { 'dataset': dataset, 'listing': listing }
                    else:
                        folderlist[dataset]['listing'].append(uri)
                filecount += 1
            if 'nextPageToken' in bucketlist:
                token = bucketlist['nextPageToken']
            else:
                token = None
    return folderlist

def sorted_list_from_dict(thedict):
    '''
       Return the keys for a dict in a sorted list.
    '''
    thelist = []
    for key in thedict:
        thelist.append(key)
    thelist.sort()
    return thelist

def multiple_runs_list(folderdict):
    '''
       Get the list of folders that have more than one set of processed files (more than
       one file for the data set ending in '-aa').
    '''
    datasetlist = sorted_list_from_dict(folderdict)
    dupeslist = []
    for dataset in datasetlist:
        j = 0
        for file in folderdict[dataset]['listing']:
            if file.rfind('-aa') == len(file)-3:
                j += 1
        if j>1:
            dupeslist.append(dataset)

    cleanuplist = []
    for dataset in dupeslist:
        j = 0
        patterns = set([])
        for file in folderdict[dataset]['listing']:
            if file.rfind('-aa') == len(file)-3:
                j += 1
                patterns.add(file[0:len(file)-3])
        newpatterns = list(patterns)
        newpatterns.sort()
        cleanuplist.append(newpatterns[0])
    return cleanuplist

def matching_file_list(folderdict, pattern):
    filelist = []
    datasetlist = sorted_list_from_dict(folderdict)
    for dataset in datasetlist:
        for file in folderdict[dataset]['listing']:
            if pattern in file:
                shard = file[len('gs://vertnet-harvesting/'):len(file)]
                filelist.append(shard)
    return filelist
    
def load_folders_in_bigquery(cs, folderdict):
    '''
       Load data from all shards in folderdict into the dumps data set in 
       BigQuery.
    '''
    # Load BigQuery table schema from file
    schema = get_schema()
    if schema is None:
        return

    # BigQuery naming
    dataset_name = 'dumps'
    table_version = format(datetime.today(), '%Y%m%d')
    table_name = 'full_{0}'.format(table_version)
    table_name = 'vertnet_latest'
    load_jobs = {}

    # Create the dumps dataset if it doesn't exist
    bq = BQ.BigQuery(bq_cred)
    print "Creating dataset '{0}'".format(dataset_name)
    bq.create_dataset(dataset_name)
        
    # Launch a load job for each harvest folder
    for folder in folderdict:
#       if folder in ['processed/ROM/e0dbf705-cec4-4dce-a152-fc4ebe14674d', \
#         'processed/KU/8f79c802-a58c-447f-99aa-1d6a0790825a', \
#         'processed/FMNH/36f15a36-6b45-442e-9c31-cd633423aee0']:
        print 'Loading: %s' % folder
        uri_list = folderdict[folder]['listing']
        # Launch a job for loading all the chunks in a single folder
        job_id = bq.create_load_job(ds_name=dataset_name,
                                    table_name=table_name,
                                    uri_list=uri_list,
                                    schema=schema)              
        
        # Store the job_id in the dictionary of job_ids
        load_jobs[folder] = job_id
        time.sleep(1)
    
    # Wait until all jobs finish
    bq.wait_jobs(10)
    
    # Check failed jobs
    failed_resources = check_failed(bq, load_jobs)
    
    # Commented out the following, as it was loading resources many times over. 
    # Work-around for failed resources is to put in a folder filter in the for block
    # above to try again to load failed resources on a subsequent run of the script. 
    # Should try to implement that here instead, doing same loop on resources in 
    # failed_resources list.
    # If any resource failed, run individual jobs for each chunk
#     if len(failed_resources) > 0:
#         # For each failed resource, launch an individual job for each chunk
#         for resource in failed_resources:
#             
#             # Build a list containing the URIs of the shards of a single resource
#             uri_list = build_uri_list(cs, resource)
#             
#             # For each uri (individual chunk)
#             for uri in uri_list:
#                 # Launch a load job
#                 job_id = bq.create_load_job(ds_name=dataset_name,
#                                     table_name=table_name,
#                                     uri_list=uri_list,
#                                     schema=schema)              
#                 # Store the job_id in the dictionary of job_ids
#                 load_jobs[uri] = job_id
#                 time.sleep(1)
#         
#         # Wait until all jobs finish
#         bq.wait_jobs(10)
#         
#         # Reset the job_ids dictionary
#         load_jobs = {}
    
    if len(failed_resources) > 0:
        dump_file = './data/failed.txt'
        print "Some chunks could not be loaded into BigQuery."
        with open(dump_file, 'w') as w:
            for i in failed_resources:
                w.write(i)
                w.write("\n")
        print "These have been written to {0}".format(dump_file)
    
    # The end
    return

def get_schema():
    fields = index_fields()
#    schema = json.load(open(os.path.join(os.path.dirname(__file__), 'schema.json')))
#    print 'schema:\n%s' % schema
    schema = {}
    schema['fields'] = []
    for field in fields:
        entry = {}
        entry['type'] = 'STRING'
        entry['name'] = field
        schema['fields'].append(entry)
    return schema

def build_uri_list(cs, resource):
    """Build a list containing the URIs of the shards of a single resource."""
    
    print "Building list of chunks for {0}".format(resource)
    
    uri_list = []
    for i in cs.list_bucket(prefix=resource)['items']:
        uri = '/'.join(["gs:/", cs._BUCKET_NAME, i['name']])
        uri_list.append(uri)
    
    return uri_list

def check_failed(bq, load_jobs):
	# Check failed jobs
    # Reset the failed_resources list
    failed_resources = []
    for resource in load_jobs:
        job_id = load_jobs[resource]['jobReference']['jobId']
        status = bq.check_job(job_id)
        print 'job status: %s' % status
        if status['state'] == 'DONE' and 'errorResult' in status:
            print 'Resource {0} failed and job was aborted. Queued for individual load.'
            failed_resources.append(resource)
    return failed_resources

def launch_load_job(uri_list):
    """Launch a job for loading all the chunks in a single resource."""
    print "Launching load job"
    return job_id

def main():
    '''
    This script analyzes the folders in the Google Cloud vertnet-portal/processing and 
    then removes up to one older duplicate. If no duplicates are found, the script uses 
    contents of the vertnet-portal/processing folder to populate a BigQuery table 
    dumps/full_yyyymmdd. If there are no duplicate folders, expect the script to run to
    completion in 10 minutes or less.
    '''
    
    # Create a CloudStorage Manager to be able to access Google Cloud Storage based on
    # the credentials stored in cs_cred.
    cs = CS.CloudStorage(cs_cred)

    # Create a dict of processed folders on Google Cloud Storage to copy into BigQuery
    # Check for folders that have multiple harvest dates in them and clean out old 
    # versions before loading BigQuery
    processedfolders = get_all_processed_folders(cs)

    if processedfolders is None or len(processedfolders) == 0:
        print 'No processed folders found'
        return False
    else:
        print '%s processed folders:' % len(processedfolders)
        for file in processedfolders:
            print '%s' % file

    # Check for duplicate files that indicate that data sets had been 
    # post-harvest-processed more than once without cleaning up previous processed files. 
    # Files from previous runs must be removed before loading BigQuery.
    previousrunslist = multiple_runs_list(processedfolders)

    for f in previousrunslist:
        print 'Removing GCS files for: %s' % f
        filestoremove = matching_file_list(processedfolders, f)
        for f in filestoremove:
            print '  %s' % f
        remove_GCS_files(cs,filestoremove)
   
    # Check again. First Duplicates should have been removed by now. There may be 
    # additional duplicates. If there are, abort now with a message to run again.
    processedfolders = get_all_processed_folders(cs)
    previousrunslist = multiple_runs_list(processedfolders)
    if len(previousrunslist) > 0:
        print 'Processed files from previous runs still exist in GCS.'
        print 'Previous runs to remove:'
        for file in previousrunslist:
            print '  %s' % file
        print 'Run big_query_loader.py again to attempt to remove these files and upload '
        print 'to BigQuery.'
        
    # Or create a subset to process based on a particular folder in GCS. 
    # ***Caution***: The table creation logic only writes to a file called
    # full_[YYYYMMDD]. Subsequent writes on the same day add data to the existing table.
#    processedfolders = {}
#    processedfolders.update(get_processed_files(cs, 'CERMES/8f6d3a0d-10d2-44e3-8612-be219376c860'))
#    processedfolders.update(get_processed_files(cs, 'CERMES/7904180c-36c9-40ca-aed2-463e36a04df7'))
#    processedfolders.update(get_processed_files(cs, 'LSUMZ/847e2306-f762-11e1-a439-00145eb45e9a'))
#    processedfolders = get_processed_files(cs, 'CCBER')
#    processedfolders = get_processed_files(cs, 'MSB/09a17133-1487-440f-93aa-656d75877280')

    load_folders_in_bigquery(cs, processedfolders)

if __name__ == "__main__":
    main()