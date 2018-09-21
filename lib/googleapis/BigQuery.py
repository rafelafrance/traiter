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

# Adapted from https://github.com/jotegui/googleapis

# This file contains common utility functions for communicating with BigQuery

__author__ = 'Javier Otegui'
__contributors__ = "Javier Otegui, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "BigQuery.py 2016-07-26T12:38+2:00"

import os
import time
import logging
#import json

from GoogleAPI import GoogleAPI, ConfigError
from apiclient import errors


class BigQuery(GoogleAPI):
    """Wrapper class for the most common BigQuery functions."""
    
    def __init__(self, config):
        """Initialize the service."""
        
        try:
            self._PROJECT_ID = config['project_id']
        except KeyError:
            raise ConfigError("Missing configuration element: project_id")
        
        try:
            self._PROJECT_NUMBER = config['project_number']
        except KeyError:
            raise ConfigError("Missing configuration element: project_number")
        
        # Initialize GoogleAPI instance and create bigquery service
        GoogleAPI.__init__(self, 'bigquery')
        self.methods = self.get_methods()
        
        return
    
    
    def get_methods(self):
        """Print the currently available methods."""
        s = ''
        for i in dir(self):
            if not i[0].isupper() and i[0] != '_' and i != 'service':
                s += i
                s += '\t{0}'.format(getattr(self, i).__doc__)
                s += "\n"
        return s
    
    # DATASET OPERATIONS #
    
    def list_datasets(self):
        """Returns a list of available datasets."""
        datasets = []
        resp = self.service.datasets().list(projectId=self._PROJECT_NUMBER).execute()
        for dataset in resp['datasets']:
            datasets.append(dataset['datasetReference']['datasetId'])
        return datasets
    
    
    def create_dataset(self, ds_name):
        """Create a new dataset if it doesn't exist."""
        datasets = self.list_datasets()
        if ds_name in datasets:
            print "Dataset '{0}' already exists.".format(ds_name)
            return
        
        req_body = {
            "kind": "bigquery#dataset",
            "datasetReference": {
                "datasetId": ds_name
            }
        }
        req = self.service.datasets().insert(projectId=self._PROJECT_ID, body=req_body)
        req.execute()
        print "Dataset '{0}' was created".format(ds_name)
        return
    
    
    def get_dataset(self, ds_name):
        """Retrieve metadata on the given dataset."""
        req = self.service.datasets().get(projectId=self._PROJECT_ID, datasetId=ds_name)
        resp = req.execute()
        return resp
    
    
    def delete_dataset(self, ds_name, force=False):
        """Delete the given dataset. Dataset must be empty before attempting deletion. Use force=True to override."""
        req = self.service.datasets().delete(projectId=self._PROJECT_ID, datasetId=ds_name, deleteContents=force)
        resp = req.execute()
        print "Dataset '{0}' was deleted.".format(ds_name)
        return

    
    # JOB OPERATIONS #
    
    def list_jobs(self, minimal=False):
        """List all jobs available to the authenticated user."""
        projection = "minimal" if minimal is True else "full"
        req = self.service.jobs().list(projectId=self._PROJECT_ID, projection=projection)
        resp = req.execute()
        return resp
    
    
    def get_job(self, job_id):
        """Retrieve metadata on a particular job."""
        req = self.service.jobs().get(projectId=self._PROJECT_ID, jobId=job_id)
        resp = req.execute()
        return resp
    
    
    def show_running_jobs(self):
        """Show how many jobs are running."""
        try:
            running = len(self.service.jobs().list(projectId=self._PROJECT_ID, stateFilter="running", projection="minimal").execute()['jobs'])
        except KeyError:
            running = 0
        return running
    
    
    def show_pending_jobs(self):
        """Show how many jobs are pending."""
        try:
            pending = len(self.service.jobs().list(projectId=self._PROJECT_ID, stateFilter="pending", projection="minimal").execute()['jobs'])
        except KeyError:
            pending = 0
        return pending
    
    
    def show_jobs(self):
        """Show how many jobs are running, pending and done."""
        running = self.show_running_jobs()
        pending = self.show_pending_jobs()
        print "{0} jobs running.\n{1} jobs pending.".format(running, pending)
        return
    
    
    def check_job(self, job_id):
        """Check if a job is done or not, and if it is done, check if it was successful."""
        result = None
        status = self.get_job(job_id)['status']
        return status
    
    
    def wait_jobs(self, timeout = 5):
        """Halts execution of caller process until all jobs finished."""
        while True:
            pending = self.show_pending_jobs()
            running = self.show_running_jobs()
            if pending == 0 and running == 0:
                return
            else:
                print '{0} jobs running, {1} jobs pending'.format(running, pending)
            time.sleep(timeout)
        
    
    # LOAD OPERATIONS #
    
    def create_load_job(self, ds_name, table_name, uri_list, schema):
        """Creates a new job for loading a list of URIs into a table within a dataset. Returns the jobId."""
        
        # uri_list has to be a list. If uri_list is a single uri (string), convert that into a list
        if type(uri_list) == type('a'):
            uri_list = [uri_list]
        
        req_body = {
            "kind": "bigquery#job",
            "configuration": {
                "load": {
                    "destinationTable": {
                        "projectId": self._PROJECT_ID,
                        "tableId": table_name,
                        "datasetId": ds_name
                    },
                    "sourceUris": uri_list,
                    "schema": schema,
                    "fieldDelimiter": "\t",
                    "quote": ''
                }
            }
        }
        
        req = self.service.jobs().insert(projectId=self._PROJECT_ID, body=req_body)
        
        while True:
            try:
                resp = req.execute()
                return resp
            except errors.HttpError as e:
                logging.warning("Something went wrong:")
                logging.warning(e)
                logging.warning("Retrying after 3 secs")
                time.sleep(3)
        
#        job_id = resp['jobReference']['jobId']
#        print job_id
        
        return resp['jobReference']['jobId']
    
    
    def wait_load(self, job_id):
        """Wait for a specific job to finish."""
        while True:
            job = self.get_job(job_id)
            if 'DONE' == job['status']['state']:
                print 'Done Loading!'
                return
                
            print 'Waiting for loading to complete...'
            time.sleep(10)

            if 'errorResult' in job['status']:
                print 'Error loading table: ', pprint.pprint(job)
                return
    
    
    # QUERY OPERATIONS #
    
    def printTableData(self, resp, row):
        """Print a single row of data."""
        row_data = resp['rows'][row]
    
    
    def run_sync_query(self, query, timeout=0):
        """Create a synchronous query job. See https://developers.google.com/bigquery/querying-data#syncqueries for details on sync queries."""
        job_body = {
            "query": query,
            "timeoutMs": timeout
        }
        req = self.service.jobs().query(projectId=self._PROJECT_ID, body=job_body)
        resp = req.execute()
        
        job_ref = resp['jobReference']
        
        # Timeout exceeded
        while not resp['jobComplete']:
            resp = self.service.jobs().getQueryResults(
                projectId=self._PROJECT_ID,
                jobId=job_ref['jobId'],
                timeoutMs=timeout).execute()
                
        # If the result has rows, print the rows in the reply.
        print resp
        if('rows' in resp):
            printTableData(resp, 0)
            currentRow = len(resp['rows'])

            # Loop through each page of data
            while 'rows' in resp and currentRow < resp['totalRows']:
                resp = self.service.jobs().getQueryResults(
                    projectId=self._PROJECT_ID,
                    jobId=job_ref['jobId'],
                    startIndex=currentRow).execute()
                if('rows' in resp):
                    printTableData(resp, currentRow)
                    currentRow += len(resp['rows'])
        
        return

    
    
    def run_async_query(self):
        """Create a synchronous query job. See https://developers.google.com/bigquery/querying-data#asyncqueries for details on sync queries."""
        pass
    
    
    def run_query_to_table(self, query, dataset_name, table_name, priority="INTERACTIVE"):
        """Runs a query and stores the output in a new table."""
        
        # Specify the job's properties
        job_body = {
            "configuration": {
                "query": {
                    "useQueryCache": True,
                    "destinationTable": {
                        "projectId": self._PROJECT_ID,
                        "tableId": table_name,
                        "datasetId": dataset_name
                    },
                    "priority": priority,
                    "allowLargeResults": True,
                    "query": query
                }
            }
        }
        
        # Launch the job
        req = self.service.jobs().insert(projectId=self._PROJECT_ID, body=job_body)
        resp = req.execute()
        
        return resp
    
    
    # EXTRACT OPERATIONS #
    
    def extract_table(self, dataset_name, table_name, bucket_name, object_name, printHeader="TRUE", destinationFormat="CSV", fieldDelimiter=",", compression="NONE"):
        """Exports the given table to a cloud storage object."""
        
        # Build destination URI
        destinationUris = ["/".join(['gs:/', bucket_name, object_name])]
        
        # Specify the job's properties
        job_body = {
            "configuration": {
                "extract": {
                    "compression": compression,
                    "fieldDelimiter": fieldDelimiter,
                    "destinationFormat": destinationFormat,
                    "printHeader": printHeader,
                    "destinationUris": destinationUris,
                    "sourceTable": {
                        "projectId": self._PROJECT_ID,
                        "tableId": table_name,
                        "datasetId": dataset_name
                    }
                }
            }
        }
        
        # Launch the job
        req = self.service.jobs().insert(projectId=self._PROJECT_ID, body=job_body)
        resp = req.execute()
        
        return resp
