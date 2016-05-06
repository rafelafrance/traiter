#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
import re
import htmlentitydefs
import os
import codecs
import unicodedata
from datetime import datetime
from google.appengine.api import namespace_manager
from google.appengine.api import search
from google.appengine.api.search import SortOptions, SortExpression
from mapreduce import operation as op
from mapreduce import context

IS_DEV = 'Development' in os.environ['SERVER_SOFTWARE']

FULL_TEXT_KEYS_OMIT = [
'title', 'eml', 'orgcountry', 'orgstateprovince'
]

# The expected header of the output file
HEADER = [
'icode', 'title', 'citation', 'contact', 'dwca', 'email', 'eml', 'emlrights', 
'gbifdatasetid', 'gbifpublisherid', 'doi', 'iptlicense', 'migrator', 'networks', 
'orgcountry', 'orgname', 'orgstateprovince', 'pubdate', 'source_url', 'url', 'id', 
'associatedmedia', 'associatedoccurrences', 'associatedorganisms', 
'associatedreferences', 'associatedsequences', 'associatedtaxa', 'bed', 'behavior',
'catalognumber', 'continent', 'coordinateprecision', 'coordinateuncertaintyinmeters', 
'country', 'countrycode', 'county', 'dateidentified', 'day', 'decimallatitude', 
'decimallongitude', 'disposition', 'earliestageorloweststage',
'earliesteonorlowesteonothem', 'earliestepochorlowestseries', 
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
'minimumelevationinmeters', 'month', 'municipality', 'occurrenceID', 'occurrenceremarks',
'occurrencestatus', 'organismid', 'organismname', 'organismremarks', 'organismscope', 
'othercatalognumbers', 'pointradiusspatialfit', 'preparations', 'previousidentifications',
'recordedby', 'recordnumber', 'reproductivecondition', 'samplingeffort', 
'samplingprotocol', 'sex', 'startdayofyear', 'stateprovince', 'typestatus', 
'verbatimcoordinates', 'verbatimcoordinatesystem', 'verbatimdepth', 'verbatimelevation', 
'verbatimeventdate', 'verbatimlatitude', 'verbatimlocality', 'verbatimlongitude', 
'verbatimsrs', 'waterbody', 'year', 'type', 'modified', 'language', 'license', 
'rightsholder', 'accessrights', 'bibliographiccitation', 'references', 'institutionid', 
'collectionid', 'datasetid', 'institutioncode', 'collectioncode', 'datasetname', 
'ownerinstitutioncode', 'basisofrecord', 'informationwithheld', 'datageneralizations',
'dynamicproperties', 'taxonid', 'scientificnameid', 'acceptednameusageid', 
'parentnameusageid', 'originalnameusageid', 'nameaccordingtoid', 'namepublishedinid', 
'taxonconceptid', 'scientificname', 'acceptednameusage', 'parentnameusage', 
'originalnameusage', 'nameaccordingto', 'namepublishedin', 'namepublishedinyear', 
'higherclassification', 'kingdom', 'phylum', 'classs', 'order', 'family', 'genus', 
'subgenus', 'specificepithet', 'infraspecificepithet', 'taxonrank', 'verbatimtaxonrank',
'scientificnameauthorship', 'vernacularname', 'nomenclaturalcode', 'taxonomicstatus', 
'nomenclaturalstatus', 'taxonremarks', 'haslength', 'haslifestage', 'hasmass', 
'hassex', 'lengthinmm', 'massing', 'lengthunitsinferred', 'massunitsinferred',
'derivedlifestage', 'derivedsex']

def is_float(str):
    """Return the value of str as a float if possible, otherwise return None."""
    # Accepts str as string. Returns float(str) or None
    if str is None:
        return None
    try:
        f = float(str)
        return f
    except ValueError:
        return None
 
def is_int(str):
    """Return the value of str as an int if possible, otherwise return None."""
    # Accepts str as string. Returns int(str) or None
    if str is None:
        return None
    try:
        f = int(str)
        return f
    except ValueError:
        return None
 
def valid_year(year):
    """Return True if the year is since 1700 and before next year, otherwise return False."""
    # Accepts year as string.
    fyear = is_float(year)
    if fyear is None:
        return False
    if fyear < 1699:
        return False
    if fyear > datetime.now().year:
        return False
    return True
 
def valid_month(month):
    """Return True if the month is between 1 and 12 inclusive, otherwise return False."""
    # Accepts month as string.
    fmonth = is_float(month)
    if fmonth is None:
        return False
    if fmonth < 1:
        return False
    if fmonth > 12:
        return False
    return True

def valid_day(day):
    """Return True if the day is between 1 and 31 inclusive, otherwise return False."""
    # Accepts day as string.
    fday = is_float(day)
    if fday is None:
        return False
    if fday < 1:
        return False
    if fday > 31:
        return False
    return True

def valid_dayofyear(dayofyear):
    """Return True if the dayofyear is between 1 and 366 inclusive, 
       otherwise return False."""
    # Accepts dayofyear as string.
    fdayofyear = is_float(dayofyear)
    if fdayofyear is None:
        return False
    if fdayofyear < 1:
        return False
    if fdayofyear > 366:
        return False
    return True

def leap_year(year):
    # Assumes year passes valid_year()
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False

def start_day_of_year(rec):
    """Return the the start day of year based on year, month, and day if there is no
        current startdayofyear or if it is not a valid day of year."""
    if rec.has_key('startdayofyear'):
        if valid_dayofyear(rec['startdayofyear']):
            return is_int(rec['startdayofyear'])
    return days_of_year(rec)
    
def end_day_of_year(rec):
    """Return the the end day of year based on year, month, and day if there is no
        current enddayofyear or if it is not a valid day of year."""
    if rec.has_key('enddayofyear'):
        if valid_dayofyear(rec['enddayofyear']):
            return is_int(rec['enddayofyear'])
    return days_of_year(rec)
    
def days_of_year(rec):
    """Return the the day of year based on year, month, and day."""
    if rec.has_key('day') == False or valid_day(rec['day'] == False):
        return None
    if rec.has_key('month') == False or valid_month(rec['month']) == False:
        return None
    if rec.has_key('year') == False or valid_year(rec['year']) == False:
        return None
    # Should have naively valid values for day, month, and year at this point.
    # Should also have no valid values in start or end day of year.
    return day_of_year(rec['day'], rec['month'], rec['year'])

def day_of_year(day, month, year):
    # Assumes day passes valid_day(), month is passes valid_month(),
    # and year passes valid_year()
    year = is_int(year)
    month = is_int(month)-1
    day = is_int(day)
    leap = 0
    if leap_year(year) and month>1:
       leap = 1
    firsts = [0,31,59,90,120,151,181,212,243,273,304,334]
    return firsts[month]+day+leap

def valid_latlng(lat,lng):
    """Return True if lat and lng are in valid ranges, otherwise return False."""
    # Accepts lat and lng as strings.
    flat = is_float(lat)
    if flat is None:
        return False
    if flat < -90 or flat > 90:
        return False
    flng = is_float(lng)
    if flng is None:
        return False
    if flng < -180 or flng > 180:
        return False
    if flat == 0 and flng == 0:
        return False
    return True
 
def valid_coords(rec):
    """Return True if decimallatitude and decimallongitude in rec are in valid ranges, otherwise return False."""
    if rec.has_key('decimallatitude'):
        if rec.has_key('decimallongitude'):
            return valid_latlng(rec['decimallatitude'],rec['decimallongitude'])
    return False
 
def valid_georef(rec):
    """Return True if rec has valid coords, valid coordinateuncertaintyinmeters, and a geodeticdatum, otherwise return False."""
    if rec.has_key('coordinateuncertaintyinmeters') is False:
        return False
    if rec.has_key('geodeticdatum') is False:
        return False
    if _coordinateuncertaintyinmeters(rec['coordinateuncertaintyinmeters']) is None:
        return False
    if rec.has_key('decimallatitude') is False:
        return False
    if rec.has_key('decimallongitude') is False:
        return False
    return valid_latlng(rec['decimallatitude'],rec['decimallongitude'])
 
def valid_binomial(rec):
    """Return True if rec has a genus and specificepithet, otherwise return False."""
    if rec.has_key('genus') is False:
        return False
    if rec.has_key('specificepithet') is False:
        return False
    # Sufficient condition for now to have these DwC terms populated.
    # Later may want to test them against a name authority to determine validity.
    # Note that this does not account for a scientificName that is not null where the 
    # genus is null.
    return True
    
def _rank(rec):
    """Return the rank to be used in document sorting based on the content priority."""
    hasbinomial = valid_binomial(rec)
    if hasbinomial is False:
        return 0
    # Must have a binomial to have a rank.
    rank = 0
    hasgeoref = valid_georef(rec)
    hascoords = False
    if hasgeoref is True:
        hascoords = True
    else:
        hascoords = valid_coords(rec) 
    hasyear = False
    if rec.has_key('year'):
        hasyear = valid_year(rec['year'])
    hasmonth = False
    if rec.has_key('month'):
        hasmonth = valid_month(rec['month'])
    hasday = False
    if rec.has_key('day'):
        hasday = valid_day(rec['day'])
    
    if hasgeoref is True:
        rank = 9
        if hasyear is True:
            rank = 10
            if hasmonth is True:
                rank = 11
                if hasday is True:
                    rank = 12
    elif hascoords is True:
        rank = 5
        if hasyear is True:
            rank = 6
            if hasmonth is True:
                rank = 7
                if hasday is True:
                    rank = 8
    else:
        rank = 1
        if hasyear is True:
            rank = 2
            if hasmonth is True:
                rank = 3
                if hasday is True:
                    rank = 4
    return rank

def has_media(rec):
    """Return 1 if the rec represents a media record or has associated media, otherwise return 0."""
    if rec.has_key('associatedmedia'):
        return 1
    if rec.has_key('type'):
        if rec['type'].lower()=='sound':
            return 1
        if 'image' in rec['type'].lower():
            return 1
        return 0
    if rec.has_key('basisofrecord'):
        if rec['basisofrecord'].lower()=='machineobservation':
            return 1
    return 0

tissuetokens = ["+t", "tiss", "tissue", "blood", "dmso", "dna", "extract", "froze",
                "frozen", "forzen", "freez", "freeze", "heart", "muscle", "higado", 
                "kidney", "liver", "lung", "nitrogen", "pectoral", "rinon", "riñon",
                "kidney", "rnalater", "sample", "sangre", "toe", "spleen"]

def has_tissue(rec):
    """Return 1 if the rec represents a record that has preparations that might be viable tissues, otherwise return 0."""
    if rec.has_key('preparations'):
        preps = rec['preparations'].lower()
        for token in tissuetokens:
            if token in preps:
                return 1
    return 0

def has_license(rec):
    """Return 1 if the rec has the iptlicense or the license field populated, otherwise return 0."""
    if rec.has_key('license'):
        return 1
    if rec.has_key('iptlicense'):
        return 1
    return 0

def was_captive(rec):
    """Return 1 if the rec has evidence that the organism was captive, otherwise return 0."""
    if rec.has_key('establishmentmeans'):
        if 'capt' in rec['establishmentmeans'].lower():
          return 1
        if 'managed' in rec['establishmentmeans'].lower():
          return 1
    if rec.has_key('locality'):
        if 'captive' in rec['locality'].lower():
          return 1
    if rec.has_key('highergeography'):
        if 'captive' in rec['highergeography'].lower():
          return 1
    return 0

def has_key(rec, key):
    """Return 1 if the rec has the key field populated, otherwise return 0."""
    if rec.has_key(key):
        return 1
    return 0

def is_fossil(rec,res_id):
    """Return 1 if the rec represents a record that is a fossil."""
    if rec.has_key('basisofrecord'):
        if 'fossil' in rec['basisofrecord'].lower():
            return 1
    return 0

def _coordinateuncertaintyinmeters(unc):
    """Return the value of unc as a rounded up integer if it is a number greater than zero, otherwise return None."""
    uncertaintyinmeters = is_float(unc)
    if uncertaintyinmeters is None:
        return None
    # Check to see if uncertaintyinmeters is less than one. Zero is not a legal 
    # value. Less than one is an error in concept.
    if uncertaintyinmeters < 1:
        return None
    # Return the nearest rounded up meter.
    return int( round(uncertaintyinmeters + 0.5) )

### This will have to stay in the indexer
def _location(lat, lon):
    """Return a GeoPoint representation of lat and long if possible, otherwise return None."""
    try:
        location = apply(search.GeoPoint, map(float, [lat, lon]))
    except:
        location = None
    return location

def _type(rec):
    """Return one of 'specimen', 'observation', or 'both' based on content of the type and basisofrecord fields."""
    if rec.has_key('basisofrecord'):
        if 'obs' in rec['basisofrecord'].lower():
            return 'observation'
        return 'specimen'
    if rec.has_key('dctype'):
        if 'obj' in rec['dctype'].lower():
            return 'specimen'
        if 'spec' in rec['dctype'].lower():
            return 'specimen'
        return 'observation'
    return 'both'

def eventdate_from_ymd(y,m,d):
    """Return the eventdate as ISO8601 based on year y, month m, and day d as strings."""
    if valid_year(y) is False:
        return None
    hasmonth = valid_month(m)
    hasday = valid_day(d)
    eventdate = y
    if hasmonth is True:
        month = is_float(m)
        if month is not None:
            if month > 9:
                eventdate += '-'+m
            else:
                eventdate += '-0'+m
            if hasday is True:
                day = is_float(d)
                if day is not None:
                    if day > 9:
                        eventdate += '-'+d
                    else:
                        eventdate += '-0'+d
    return eventdate
    
def _eventdate(rec):
    """Return the eventdate as a datetime.date based on a eventdate if it is a datetime, otherwise on year, month, and day converted to ISO8601."""
    isodate = None
    if rec.has_key('eventdate'):
        isodate = rec['eventdate']
    else:
        if rec.has_key('year') is False or rec.has_key('month') is False or rec.has_key('day') is False:
            return None
            y = rec['year']
            m = rec['month']
            d = rec['day']
            isodate = eventdate_from_ymd(y,m,d)
    
    try:
        eventdate = datetime.strptime(isodate, '%Y-%m-%d').date()
    except:
        eventdate = None        
    return eventdate

def slugify(s, length=None, separator="-"):
    """Return a slugged version of supplied string."""
    s = re.sub('[^a-zA-Z\d\s:]', ' ', s)
    if length:
        words = s.split()[:length]
    else:
        words = s.split()
    s = ' '.join(words)
    ret = ''
    for c in s.lower():
        try:
            ret += htmlentitydefs.codepoint2name[ord(c)]
        except:
            ret += c
    ret = re.sub('([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)', r'\1', ret)
    ret = ret.strip()
    ret = re.sub(' ', '_', ret)
    ret = re.sub('\W', '', ret)
    ret = re.sub('[ _]+/', separator, ret)
    return ret.strip()

def get_rec_dict(rec):
    """Returns a dictionary of all fields in the rec list with non-printing characters removed."""
    val = {}
    for name, value in rec.iteritems():
        if value:
        	# Replace all tabs, vertical tabs, carriage returns, and line feeds 
        	# in field contents with space, then remove leading and trailing spaces.
            val[name] = re.sub('[\v\t\r\n]+', ' ', value).strip(' ')
#            if val[name]=='':
#                rec.pop(name)
    return val

    @classmethod
    def initalize(cls, resource):
        namespace = namespace_manager.get_namespace()
        filename = '/gs/vn-indexer/failures-%s-%s.csv' % (namespace, resource)
        log = cls.get_or_insert(key_name=filename, namespace=namespace)
        return log

def verbatim_dwc(rec, keyname):
    """Returns a record with verbatim original Darwin Core fields plus the keyname field, minus any empty fields."""
#    logging.info('In verbatim_dwc, rec: %s' % (rec))
    for key in rec.keys():
        if rec[key] == '' or key in FULL_TEXT_KEYS_OMIT:
            rec.pop(key)
    rec['keyname'] = keyname
    return rec

def index_record(data, indexdate, issue=None):
    """Creates a document ready to index from the given input data. This is where the 
       work is done to construct the document."""
    occid, icode, collcode, catnum, \
    gbifdatasetid, gbifpublisherid, networks, \
    license, iptlicense, migrator, \
    dctype, basisofrecord, references, \
    continent, country, stateprov, county, municipality, \
    islandgroup, island, waterbody, locality, \
    lat, lon, uncertainty, \
    geodeticdatum, georeferencedby, georeferenceverificationstatus, \
    kingdom, phylum, classs, order, family, \
    genus, specep, infspecep, \
    scientificname, vernacularname, typestatus, \
    year, month, day, \
    collname, recordnumber, fieldnumber, \
    bed, formation, group, member, \
    sex, lifestage, preparations, reproductivecondition, \
    startdayofyear, enddayofyear, \
    haslength, haslifestage, hasmass, hassex, \
    lengthinmm, massing = map(data.get, 
        ['id', 'icode', 'collectioncode', 'catalognumber', 
         'gbifdatasetid', 'gbifpublisherid', 'networks', 
         'license', 'iptlicense', 'migrator',
         'type', 'basisofrecord', 'references', 
         'continent', 'country', 'stateprovince', 'county', 'municipality', 
         'islandgroup', 'island', 'waterbody', 'locality',
         'decimallatitude', 'decimallongitude', 'coordinateuncertaintyinmeters', 
         'geodeticdatum', 'georeferencedby', 'georeferenceverificationstatus',
         'kingdom', 'phylum', 'classs', 'order', 'family', 
         'genus', 'specificepithet', 'infraspecificepithet', 
         'scientificname', 'vernacularname', 'typestatus', 
         'year', 'month', 'day', 
         'recordedby', 'recordnumber', 'fieldnumber',
         'bed', 'formation', 'group', 'member',
         'sex', 'lifestage', 'preparations', 'reproductivecondition',
         'startdayofyear', 'enddayofyear',
         'haslength', 'haslifestage', 'hasmass', 'hassex', 
         'lengthinmm', 'massing'])
    
    # Translate the field 'classs' to field 'class'
#     if data.has_key('classs'):        
#         data.pop('classs')
#     data['class'] = classs

    # Translate the field 'type' to field 'dctype'
#     if data.has_key('type'):
#         data.pop('type')
#     data['dctype'] = dctype

    # Translate the field 'iptlicense' to field 'license' if the latter is missing
#     if (license is None or len(data[license]) == 0) and iptlicense is not None:
#       license = iptlicense

    # Create a slugged version of the resource title as a resource identifier
#     resource_slug = slugify(data['title'])    
#     icode_slug = re.sub(" ","", icode.lower())
    
    # Make a coll_id as slugged ascii of the collection for use in document id.
#     coll_id = ''
#     if collcode is not None and collcode != '':
#         coll_id = re.sub(' ','-', re.sub("\'",'',repr(collcode)).lower())
#     else:
#         coll_id = re.sub("\'",'',repr(resource_slug))
    
    # Make a occ_id as slugged ascii of the record identifier for use in document id.
#     occ_id = ''
#     if catnum is not None and len(catnum) > 0:        
#         occ_id = re.sub("\'",'',repr(slugify(data['catalognumber'])))
#     else:
#         if occid is not None and len(occid) > 0:
#             occ_id = 'oid-%s' % re.sub("\'",'',repr(occid))
#         else:
#             occ_id = 'noid'

    # Make a potentially persistent resource identifier
#     res_id = '%s/%s' % (icode_slug, resource_slug)

    # Make a unique, potentially persistent document id
#     keyname = '%s/%s/%s' % (icode_slug, coll_id, occ_id)
#     data['keyname'] = keyname
#     # VertNet migrator must construct the references field using this same pattern for 
#     # records that do not already have a references value.
#     if references is None or len(references)==0:
#       references = 'http://portal.vertnet.org/o/%s/%s?id=%s' % (icode_slug, coll_id, occ_id)

    # Determine any values for indexing that must be calculated before creating doc
    # because full_text_key_trim(data) affects the contents of data.
#    recrank = _rank(data)
    ### Note: The location is one thing that must be processed in the indexer.
    location = _location(lat, lon)
#    unc = _coordinateuncertaintyinmeters(uncertainty)
    ### Note: The eventdate is one thing that must be processed in the indexer, because
    #         here it needs to be a datetime for query purposes.
    eventdate = _eventdate(data)
    ### Note: The year, month and day must be processed in the indexer, because
    #         here they need to be a numbers for query purposes.
    fyear = is_float(year)
    fmonth = is_float(month)
    fday = is_float(day)

    # Do full text indexing on all the verbatim fields of the record. 
    # Index specific key fields for explicit searches on their content.
    # hashid is a hash of the keyname as a means to evenly distribute records among bins
    # for parallel processing with bins having 10k or less records as recommended by 
    # Google engineers.

    doc = search.Document(
        doc_id=keyname,
        rank=recrank,
		fields=[
                search.TextField(name='iptrecordid', value=occid),
                search.TextField(name='institutioncode', value=icode),
                search.TextField(name='collectioncode', value=collcode),
                search.TextField(name='catalognumber', value=catnum),
                
                search.TextField(name='gbifdatasetid', value=gbifdatasetid),
                search.TextField(name='gbifpublisherid', value=gbifpublisherid),
                search.TextField(name='networks', value=networks),
                search.TextField(name='lastindexed', value=indexdate),                

                search.TextField(name='license', value=license),
                search.TextField(name='iptlicense', value=iptlicense),
                search.TextField(name='migrator', value=migrator),

                search.TextField(name='dctype', value=dctype),
                search.TextField(name='basisofrecord', value=basisofrecord),
                search.TextField(name='type', value=_type(data)),

                search.TextField(name='continent', value=continent),
                search.TextField(name='country', value=country),
                search.TextField(name='stateprovince', value=stateprov),
                search.TextField(name='county', value=county),
                search.TextField(name='municipality', value=municipality),

                search.TextField(name='island', value=island),
                search.TextField(name='islandgroup', value=islandgroup),
                search.TextField(name='waterbody', value=waterbody),
                search.TextField(name='locality', value=locality),

                search.TextField(name='geodeticdatum', value=geodeticdatum),
                search.TextField(name='georeferencedby', value=georeferencedby),
                search.TextField(name='georeferenceverificationstatus', value=georeferenceverificationstatus),

                search.TextField(name='kingdom', value=kingdom),
                search.TextField(name='phylum', value=phylum),
                search.TextField(name='class', value=classs),
                search.TextField(name='order', value=order),
                search.TextField(name='family', value=family),

                search.TextField(name='genus', value=genus),
                search.TextField(name='specificepithet', value=specep),
                search.TextField(name='infraspecificepithet', value=infspecep),

                search.TextField(name='scientificname', value=scientificname),
                search.TextField(name='vernacularname', value=vernacularname),
                search.TextField(name='typestatus', value=typestatus),

                search.TextField(name='recordedby', value=collname),
                search.TextField(name='recordnumber', value=recordnumber),
                search.TextField(name='fieldnumber', value=fieldnumber),

                search.TextField(name='bed', value=bed),
                search.TextField(name='formation', value=formation),
                search.TextField(name='group', value=group),
                search.TextField(name='member', value=member),

                search.TextField(name='sex', value=sex),
                search.TextField(name='lifestage', value=lifestage),
                search.TextField(name='preparations', value=preparations),
                search.TextField(name='reproductivecondition', value=reproductivecondition),

                search.NumberField(name='haslength', value=is_int(haslength)),
                search.NumberField(name='haslifestage', value=is_int(haslifestage)),
                search.NumberField(name='hasmass', value=is_int(hasmass)),
                search.NumberField(name='hassex', value=is_int(hassex)),
                search.NumberField(name='lengthinmm', value=is_float(lengthinmm)),
                search.NumberField(name='massing', value=is_float(massing)),

                search.NumberField(name='startdayofyear', value=start_day_of_year(data)),
                search.NumberField(name='enddayofyear', value=end_day_of_year(data)),

                search.NumberField(name='media', value=has_media(data)),
                search.NumberField(name='tissue', value=has_tissue(data)),
                search.NumberField(name='fossil', value=is_fossil(data,res_id)),
                search.NumberField(name='hastypestatus', value=has_key(data, 'typestatus')),
                search.NumberField(name='wascaptive', value=was_captive(data)),
                search.NumberField(name='haslicense', value=has_license(data)),

                search.NumberField(name='rank', value=recrank),
                search.NumberField(name='hashid', value=hash(keyname)%1999),
                search.TextField(name='verbatim_record', 
                                 value=json.dumps(verbatim_dwc(data, keyname)))])

    mappable = 0
    if location is not None:
        doc.fields.append(search.GeoField(name='location', value=location))
        mappable = 1
    doc.fields.append(search.NumberField(name='mappable', value=mappable))

    if unc is not None:
        doc.fields.append(search.NumberField(name='coordinateuncertaintyinmeters', value=unc))

    if fyear is not None:
        doc.fields.append(search.NumberField(name='year', value=fyear))

    if fmonth is not None:
        doc.fields.append(search.NumberField(name='month', value=fmonth))

    if fday is not None:
        doc.fields.append(search.NumberField(name='day', value=fday))

    if eventdate is not None:
        doc.fields.append(search.DateField(name='eventdate', value=eventdate))
    return doc

def index_doc(doc, index_name, namespace, issue=None):
    max_retries = 2
    retry_count = 0
    while retry_count < max_retries:
        try:
            search.Index(index_name, namespace=namespace).put(doc)
            logging.warning('Indexed doc:\n%s' % doc )
            return # Successfully indexed document.
        except Exception, e:
            logging.error('Put #%s failed for doc %s (%s)' % (retry_count, doc.doc_id, e))
            retry_count += 1
    logging.error('Failed to index: %s' % doc.doc_id)

def build_search_index(readbuffer):
    # readbuffer should be a tuple from GoogleCloudLineInputReader composed of a
    # tuple of the form ((file_name, offset), line)

    # Get namespace from mapreduce job and set it.
    ctx = context.get()
    params = ctx.mapreduce_spec.mapper.params
    namespace = params['namespace']
    index_name = params['index_name']
    rightnow=datetime.now()
    today=rightnow.day
    if today < 10:
      day='0%s' % today
    else:
      day='%s' % today
    thismonth=rightnow.month
    if thismonth < 10:
      month='0%s' % thismonth
    else:
      month='%s' % thismonth
    indexdate='%s-%s-%s'  % (rightnow.year, month, day)

    try:
        # Get the row out of the input buffer
        row=readbuffer[1]
        # Create a dictionary from the HEADER and the row
        data = get_rec_dict(dict(zip(HEADER, row.split('\t'))))
#        logging.warning('Data from %s offset %s: %s' % (readbuffer[0][0], readbuffer[0][1], data))
        # Create an index document from the row dictionary
        doc = index_record(data, indexdate)
        # Store the document in the given index
        index_doc(doc, index_name, namespace)
    except Exception, e:
        logging.error('%s\n%s' % (e, readbuffer))

def _get_rec(doc):
    for field in doc.fields:
        if field.name == 'record':
            rec = json.loads(field.value)
            rec['rank'] = doc._rank
            return rec

def delete_entity(entity):
    yield op.db.Delete(entity)