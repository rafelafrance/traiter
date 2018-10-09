googleapis
==========

Python wrapper classes for accessing different Google Cloud APIs (https://developers.google.com/api-client-library/)

Installation
------------

Install the Google API Client for Python via pip or easy_install:

    $ pip install --upgrade google-api-python-client

or

    $ easy_install --upgrade google-api-python-client

This module (the whole folder) should be available to Python by adding the parent folder to the PYTHONPATH environment variable.

Requirements
------------

For the APIs to work, a client_secrets.json file must be present in the working folder, with client id and secrets. These can be obtained from the Cloud Console (https://console.developers.google.com), under "APIs & auth" / "Credentials". The file _must_ be named 'client_secrets.json'

Besides, each module requires providing some configuration values. Specifically:

* BigQuery requires the project_id and the project_number. Both can be obtained from the Cloud Console
* CloudStorage requires a bucket_name

These should be provided in the form of a dictionary with the aforementioned keys. My personal recommendation is to create a module named cred.py with two dictionaries, one for each service:

    [in cred.py]
    bq_cred = {
        "project_number": 1234,
        "project_id": "XXXX"
    }
    
    cs_cred = {
        "bucket_name": "XXXX"
    }

How it works
------------

Simply import the class module for the specific service you will use, and the credentials

    from googleapis import BigQuery
    from cred import bq_cred

Then, initialize the service

    bq = BigQuery.BigQuery(bq_cred)

The first time an instance is initialized, it will redirect to an authentication page. The authentication mechanism will create a 'bigquery.dat' or 'storage.dat' file in the folder, to avoid having to re-authenticate every time.

Each object has a method called 'methods' that shows the available methods and a brief description.
