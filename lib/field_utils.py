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

# Adapted from https://github.com/VertNet/dwc-indexer
# This file contains definitions of field lists used in VertNet harvesting and indexing.

__author__ = "John Wieczorek"
__contributors__ = "Aaron Steele, John Wieczorek"
__copyright__ = "Copyright 2018 vertnet.org"
__version__ = "field_utils.py 2018-04-07T18:00-3:00"
from google.cloud import bigquery
     
# NOTE: The field lists here should match exactly those of 
# https://github.com/VertNet/dwc-indexer/blob/master/lib/field_utils.py

# Fields expected from the VertNet harvester output: https://github.com/VertNet/gulo
HARVEST_FIELDS = [
'icode', 'count', 'title', 'citation', 'contact', 'dwca', 'email', 'eml', 'emlrights', 
'gbifdatasetid', 'gbifpublisherid', 'doi', 'iptlicense', 'migrator', 'networks', 
'orgcountry', 'orgname', 'orgstateprovince', 'pubdate', 'source_url', 'url', 'iptrecordid', 
'associatedmedia', 'associatedoccurrences', 'associatedorganisms', 'associatedreferences', 
'associatedsequences', 'associatedtaxa', 'bed', 'behavior', 'catalognumber', 'continent', 
'coordinateprecision', 'coordinateuncertaintyinmeters', 'country', 'countrycode', 
'county', 'dateidentified', 'day', 'decimallatitude', 'decimallongitude', 'disposition', 
'earliestageorloweststage', 'earliesteonorlowesteonothem', 'earliestepochorlowestseries', 
'earliesteraorlowesterathem', 'earliestperiodorlowestsystem', 'enddayofyear', 
'establishmentmeans', 'eventdate', 'eventid', 'eventremarks', 'eventtime', 'fieldnotes', 
'fieldnumber', 'footprintspatialfit', 'footprintsrs', 'footprintwkt', 'formation', 
'geodeticdatum', 'geologicalcontextid', 'georeferencedby', 'georeferenceddate', 
'georeferenceprotocol', 'georeferenceremarks', 'georeferencesources', 
'georeferenceverificationstatus', 'group', 'habitat', 'highergeography', 
'highergeographyid', 'highestbiostratigraphiczone', 'identificationid', 
'identificationqualifier', 'identificationreferences', 'identificationremarks', 
'identificationverificationstatus', 'identifiedby', 'individualcount', 'island', 
'islandgroup', 'latestageorhigheststage', 'latesteonorhighesteonothem', 
'latestepochorhighestseries', 'latesteraorhighesterathem', 'latestperiodorhighestsystem', 
'lifestage', 'lithostratigraphicterms', 'locality', 'locationaccordingto', 'locationid', 
'locationremarks', 'lowestbiostratigraphiczone', 'materialsampleid', 
'maximumdepthinmeters', 'maximumdistanceabovesurfaceinmeters', 'maximumelevationinmeters',
'member', 'minimumdepthinmeters', 'minimumdistanceabovesurfaceinmeters', 
'minimumelevationinmeters', 'month', 'municipality', 'occurrenceid', 'occurrenceremarks', 
'occurrencestatus', 'organismid', 'organismname', 'organismremarks', 'organismscope', 
'othercatalognumbers', 'pointradiusspatialfit', 'preparations', 'previousidentifications',
'recordedby', 'recordnumber', 'reproductivecondition', 'samplingeffort', 
'samplingprotocol', 'sex', 'startdayofyear', 'stateprovince', 'typestatus', 
'verbatimcoordinates', 'verbatimcoordinatesystem', 'verbatimdepth', 'verbatimelevation', 
'verbatimeventdate', 'verbatimlatitude', 'verbatimlocality', 'verbatimlongitude', 
'verbatimsrs', 'waterbody', 'year', 'dctype', 'modified', 'language', 'license', 
'rightsholder', 'accessrights', 'bibliographiccitation', 'references', 'institutionid', 
'collectionid', 'datasetid', 'institutioncode', 'collectioncode', 'datasetname', 
'ownerinstitutioncode', 'basisofrecord', 'informationwithheld', 'datageneralizations', 
'dynamicproperties', 'taxonid', 'scientificnameid', 'acceptednameusageid', 
'parentnameusageid', 'originalnameusageid', 'nameaccordingtoid', 'namepublishedinid', 
'taxonconceptid', 'scientificname', 'acceptednameusage', 'parentnameusage', 
'originalnameusage', 'nameaccordingto', 'namepublishedin', 'namepublishedinyear', 
'higherclassification', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 
'subgenus', 'specificepithet', 'infraspecificepithet', 'taxonrank', 'verbatimtaxonrank', 
'scientificnameauthorship', 'vernacularname', 'nomenclaturalcode', 'taxonomicstatus', 
'nomenclaturalstatus', 'taxonremarks']

# Fields added for indexing
ADDED_FIELDS = [
'keyname', 'haslicense', 'vntype', 'rank', 'mappable', 'hashid',
'hastypestatus', 'wascaptive', 'wasinvasive', 'hastissue', 'hasmedia', 'isfossil',
'haslength', 'haslifestage', 'hasmass', 'hassex', 'lengthinmm', 'lengthtype', 'massing', 
'lengthunitsinferred', 'massunitsinferred', 'underivedlifestage', 'underivedsex',
'isarch']

# Fields to remove from indexing
REMOVE_FIELDS = [
'count', 'dwca', 'eml', 'iptlicense', 'url', 'taxonid', 'acceptednameusageid', 
'parentnameusageid', 'originalnameusageid', 'nameaccordingtoid', 'taxonconceptid', 
'parentnameusage', 'nameaccordingto', 'nomenclaturalstatus', 'taxonremarks']

# Fields for usage logs
LOG_SCHEMA = [
bigquery.SchemaField('cartodb_id', 'integer', 'NULLABLE', None, ()),
bigquery.SchemaField('the_geom', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('query', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('client', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('created_at', 'timestamp', 'NULLABLE', None, ()), 
bigquery.SchemaField('updated_at', 'timestamp', 'NULLABLE', None, ()), 
#bigquery.SchemaField('the_geom_webmercator', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('error', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('type', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('count', 'integer', 'NULLABLE', None, ()), 
bigquery.SchemaField('downloader', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('lat', 'float', 'NULLABLE', None, ()), 
bigquery.SchemaField('lon', 'float', 'NULLABLE', None, ()), 
bigquery.SchemaField('download', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('results_by_resource', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('matching_records', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('response_records', 'integer', 'NULLABLE', None, ()), 
bigquery.SchemaField('api_version', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('request_source', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('query_version', 'string', 'NULLABLE', None, ()), 
bigquery.SchemaField('source', 'string', 'NULLABLE', None, ())]

# Fields to go in the output
def index_fields():
    indexthese = HARVEST_FIELDS + ADDED_FIELDS
    for f in REMOVE_FIELDS:
        indexthese.remove(f)
    return indexthese

# Fields to go in the logs
def log_fields():
    return LOG_FIELDS
