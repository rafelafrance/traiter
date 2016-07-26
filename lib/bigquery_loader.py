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
__version__ = "bigquery_loader.py 2016-07-26T10:24+02:00"

from googleapis import CloudStorage as CS
from googleapis import BigQuery as BQ
from creds.google_creds import cs_cred
from creds.google_creds import bq_cred
from field_utils import index_fields
from datetime import datetime

def get_processed_files(cs, folder):
    '''
       Get the list of files in a folder of processed files to copy into BigQuery.
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
#    print 'bucket: %s\nfolders: %s' % (bucket, cs.list_bucket(prefix=resource))
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
#                    print 'itemname: %s' % item['name']
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
#                print 'nextPageToken: %s' % (token)
            else:
                token = None
    return folderlist

def check_processed_folders(folderdict):
    datasetlist = []
    dupeslist = []
    instlist = []
    for folder in folderdict:
        datasetlist.append(folder)
    datasetlist.sort()
    i = 0
    total = 0
    for dataset in datasetlist:
        i += 1
        inst = dataset.split('/')[1]
        if inst not in instlist:
            instlist.append(inst)
        print '%s) %s (%s)' % (i, dataset, len(folderdict[dataset]['listing']))
        j = 0
        dupes = 0
        for file in folderdict[dataset]['listing']:
            j +=1
            if file in dupeslist:
                print 'Remove duplicates before proceeding. Dupes found in %s.' % file
                return False
            else:
                dupeslist.append(file)
            print '  %s) %s' % (j, file)
        total += j
    print '%s Institutions:' % len(instlist)
    k = 0
    for inst in instlist:
        k += 1
        print '%s) %s' % (k, inst)
    s = '%s files found in %s folders' % (total, i)
    print '%s' % s
    print 'No duplicates found. But check data set count against expected number.'
    return True

def load_folders_in_bigquery(cs, folderdict):
    '''
       Load data from all shards in folderdict into the dumps data set in 
       BigQuery.
    '''
    # Load BigQuery table schema from file
    schema = get_schema()
#    print 'constructedschema:\n%s' % schema
    if schema is None:
        return

    # BigQuery naming
    dataset_name = 'dumps'
    table_version = format(datetime.today(), '%Y%m%d')
    table_name = 'full_{0}'.format(table_version)
    load_jobs = {}

    # Create the dumps dataset if it doesn't exist
    bq = BQ.BigQuery(bq_cred)
    print "Creating dataset '{0}'".format(dataset_name)
    bq.create_dataset(dataset_name)
        
    # Launch a load job for each harvest folder
#    print 'folderdict: %s' % folderdict
    for folder in folderdict:
        uri_list = folderdict[folder]['listing']
#        print 'uri_list: %s' % uri_list
        # Launch a job for loading all the chunks in a single folder
        job_id = bq.create_load_job(ds_name=dataset_name,
                                    table_name=table_name,
                                    uri_list=uri_list,
                                    schema=schema)              
        
        # Store the job_id in the dictionary of job_ids
        load_jobs[folder] = job_id

#    print 'job list:\n%s' % bq.list_jobs()
    
    # Wait until all jobs finish
    bq.wait_jobs(10)
    
    # Check failed jobs
    failed_resources = check_failed(bq, load_jobs)
    
    # If any resource failed, run individual jobs for each chunk
    if len(failed_resources) > 0:
        # For each failed resource, launch an individual job for each chunk
        for resource in failed_resources:
            
            # Build a list containing the URIs of the shards of a single resource
            uri_list = build_uri_list(cs, resource)
            
            # For each uri (individual chunk)
            for uri in uri_list:
                # Launch a load job
                job_id = bq.create_load_job(ds_name=dataset_name,
                                    table_name=table_name,
                                    uri_list=uri_list,
                                    schema=schema)              
                # Store the job_id in the dictionary of job_ids
                load_jobs[uri] = job_id
        
        # Wait until all jobs finish
        bq.wait_jobs(10)
        
        # Reset the job_ids dictionary
        load_jobs = {}
    
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
    Get the folders to process. Create the ./data/resource_staging.csv by exporting from
    CartoDB the results of the following query (modified to filter on harvestfoldernew, 
    for example):
      SELECT a.icode, a. gbifdatasetid, b.harvestfoldernew
      FROM resource a, resource_staging b
      WHERE 
      a.url=b.url AND
      a.ipt=True AND 
      a.networks like '%VertNet%' AND
      harvestfoldernew LIKE 'vertnet-harvesting/data/2016-07-15/%'
      order by icode, github_reponame asc
    Invoke without parameters as:
       python harvest_resource_processor.py
    '''
    # Create a CloudStorage Manager to be able to access Google Cloud Storage based on
    # the credentials stored in cs_cred.
    cs = CS.CloudStorage(cs_cred)

    # Create a dict of processed folders on Google Cloud Storage to copy into BigQuery
    processedfolders = get_all_processed_folders(cs)

    # Or create a subset to process based on a particular folder in GCS. 
    # ***Caution***: The table creation logic only writes to a file called
    # full_[YYYYMMDD]. Subsequent writes on the same day add data to the existing table.
#    processedfolders = get_processed_files(cs, 'CCBER')
#    processedfolders = get_processed_files(cs, 'test')
#    processedfolders = get_processed_files(cs, 'MVZ/f3e4b261-00c5-4f3a-a5b7-d66075b7f3e1')
#    processedfolders = get_processed_files(cs, 'UWYMV/b11cbb9e-8ee0-4d9a-8eac-da5d5ab53a31')
#    processedfolders = get_processed_files(cs, 'MSB/09a17133-1487-440f-93aa-656d75877280')
#    processedfolders = get_processed_files(cs, 'CM/6720aee6-2aad-446d-bb97-ba009d1b5666')

    if processedfolders is None or len(processedfolders) == 0:
        print 'No processed folders found'
        return False
    else:
        print 'processed folders: %s' % processedfolders
        print '%s files:' % len(processedfolders)
        for file in processedfolders:
            print '%s' % file

    if check_processed_folders(processedfolders) == False:
        print 'Aborting load until processed folder check passes.'
        return False

    load_folders_in_bigquery(cs, processedfolders)

if __name__ == "__main__":
    main()