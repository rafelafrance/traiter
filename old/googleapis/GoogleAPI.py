import argparse
import httplib2
import os
import sys
import json

from apiclient import discovery, errors
from oauth2client import file
from oauth2client import client
from oauth2client import tools

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


class ConfigError(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)


class GoogleAPI():
    """Common initialization function for all GoogleAPI specific instances."""

    def __init__(self, api):
        """Initialize the service."""

        if api == 'bigquery':
            scope = ['https://www.googleapis.com/auth/bigquery', # For BigQuery Jobs
                     'https://www.googleapis.com/auth/devstorage.read_write'] # For Cloud Storage exports
            self._API_VERSION = 'v2'
        elif api == 'storage':
            scope = ['https://www.googleapis.com/auth/devstorage.read_write']
            self._API_VERSION = 'v1'
        elif api == 'mapsengine':
            scope = ['https://www.googleapis.com/auth/mapsengine']
            self._API_VERSION = 'v1'

        argv = sys.argv
        flags = parser.parse_args(argv[1:])


        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to the file.
        self.CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
        self.FLOW = client.flow_from_clientsecrets(self.CLIENT_SECRETS, scope=scope, message=tools.message_if_missing(self.CLIENT_SECRETS))
        storage = file.Storage('{0}.dat'.format(api))
        credentials = storage.get()
        #credentials = None # Uncomment to renew credentials
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(self.FLOW, storage, flags)

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Construct the service object for the interacting with the Cloud Storage API.
        self.service = discovery.build(api, self._API_VERSION, http=http)

        return


    # TODO: test
    def safe_exec(self, req):
        """Execute a request safely, avoiding refused connections and reporting only serious problems."""
        while True:
            try:
                resp = req.execute()
                return resp
            except errors.HttpError as e:
                print "Something weird happened:"
                print e
                print "Retrying in 3 seconds"
                time.sleep(3)
