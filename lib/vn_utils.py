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
# Adapted from https://github.com/kurator-org/kurator-validation

# This file contains common utility functions for dealing with the content of VertNet
# harvested text files. It is built with unit tests that can be invoked by running the 
# script without any command line parameters. Test data are expected to be in 
# ./tests/data.
#
# Example:
#
# python vn_utils.py

__author__ = "John Wieczorek"
__contributors__ = "Aaron Steele, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "vn_utils.py 2016-07-11T14:47+2:00"

import csv
import os
import re
import logging
import unittest
import arrow # used for format_date_as_w3c()
from slugify import slugify
from datetime import datetime

# need to install arrow for this to be used (better support of date time)
# pip install arrow

def record_level_resolution(rec):
    """ Create a dictionary of completed, corrected record-level fields from data in 
        a dictionary. Also make a keynam for the index.
    parameters:
        rec - dictionary to search for record_level input (required)
    returns:
        dictionary of completed, corrected record_level fields
    """
    ### KEYNAME ###
    keyname = None    
    #  rec must contain icode
    if rec.has_key('icode') == False or len(rec['icode']) == 0:
        return None

    # rec must contain either collectioncode or gbifdatasetid
    if rec.has_key('collectioncode') == False or len(rec['collectioncode']) == 0:
        if rec.has_key('gbifdatasetid') == False or len(rec['gbifdatasetid']) == 0:
            return None

    # rec must contain either catalognumber or id
    if rec.has_key('catalognumber') == False or len(rec['catalognumber']) == 0:
        if rec.has_key('id') == False or len(rec['id']) == 0:
            return None

    # Create a condensed version of the icode from the VertNet registry as an 
    # institution identifier
    icode_slug = slugify(rec['icode'])

    # Create a condensed version of the collectioncode as a collection identifier
    # If the collectioncode has content, use it for the collection identifier
    # otherwise, use the slugged version of the resource identifier
    if rec.has_key('collectioncode') and len(rec['collectioncode']) > 0:
#        coll_id = re.sub(' ','-', re.sub("\'",'',repr(rec['collectioncode'])).lower())
        coll_id = slugify(rec['collectioncode'])
    else:
        coll_id = rec['gbifdatasetid']

    # Create a condensed version of the occurrence identifier
    # If the catalognumber has content, use it for the occurrence identifier
    # otherwise, use the id field
    bestid = None
    if rec.has_key('occurrenceid') and len(rec['occurrenceid'].strip()) > 0:
        bestid = rec['occurrenceid'].strip()
    elif rec.has_key('id') and len(rec['id'].strip()) > 0:
        bestid = rec['id'].strip()
    elif rec.has_key('catalognumber') and len(rec['catalognumber'].strip()) > 0:
        bestid = rec['catalognumber'].strip()
    else:
        bestid = 'noid'

    occ_id = slugify(bestid)

    # Make a unique, potentially persistent record (datastore document) identifier
    keyname ='%s/%s/%s' % (icode_slug, coll_id, occ_id)
    keyname = keyname.replace('//','/')

    ### REFERENCES ###
    # VertNet migrator must construct the references field using this same pattern for 
    # records that do not already have a references value.
    references = None
    if rec.has_key('references') == False or len(rec['references']) == 0 or \
       'portal.vertnet.org' in rec['references'].lower():
        references = 'http://portal.vertnet.org/o/%s/%s?id=%s' % \
          (icode_slug, coll_id, occ_id)
    else:
        references = rec['references']

    ### BASISOFRECORD ###
    # Standardize basisOfRecord
    basisofrecord = 'Occurrence'
    if rec.has_key('basisofrecord'):
        s = rec['basisofrecord'].strip().lower()
        if len(s) > 0:
            if 'preserv' in s:
                basisofrecord = 'PreservedSpecimen'
            elif 'material' in s:
                basisofrecord = 'MaterialSample'
            elif s == 'specimen':
                basisofrecord = 'PreservedSpecimen'
            elif 'machine' in s:
                basisofrecord = 'MachineObservation'
            elif 'human' in s:
                basisofrecord = 'HumanObservation'
    # Requires is_fossil() to have been used to set rec['isfossil']
    if rec.has_key('isfossil') and rec['isfossil'] == 1:
        basisofrecord = 'FossilSpecimen'

    ### DCTYPE ###
    # Standardize dc:type
    dctype = 'Event'
    if 'specimen' in basisofrecord.lower():
        dctype = 'PhysicalObject'
    elif 'material' in basisofrecord.lower():
        dctype = 'PhysicalObject'
    elif rec.has_key('dctype'):
        s = rec['dctype'].strip().lower()
        if 'moving' in s:
            dctype = 'MovingImage'
            basisofrecord = 'MachineObservation'
        elif 'still' in s:
            dctype = 'StillImage'
            basisofrecord = 'MachineObservation'
        elif s == 'sound':
            dctype = 'Sound'
            basisofrecord = 'MachineObservation'
        elif 'obj' in s:
            if 'obs' not in basisofrecord.lower():
                dctype = 'PhysicalObject'

    ### CITATION ###
    # Construct a standardized citation following the formula from the VertNet norms.
    citation = None
    title = None
    publisher = None
    link = None
    doi = None
    pubdate = None

    if rec.has_key('title') and len(rec['title'].strip()) > 0:
        title = rec['title'].strip()
    elif rec.has_key('collectioncode') and len(rec['collectioncode'].strip()) > 0:
        title = rec['collectioncode'].strip()
    else:
        title = rec['gbifdatasetid']

    if rec.has_key('orgname') and len(rec['orgname'].strip()) > 0:
        publisher = rec['orgname'].strip()
    else:
        publisher = rec['icode']

    if rec.has_key('source_url') and len(rec['source_url'].strip()) > 0:
        link = rec['source_url'].strip()

    if rec.has_key('doi') and len(rec['doi'].strip()) > 0:
        doi = rec['doi'].strip()

    if rec.has_key('pubdate') and len(rec['pubdate'].strip()) > 0:
        pubdate = rec['pubdate'].strip()

    s = ''
    if title is not None:
        s += '%s. ' % title 
    if publisher is not None:
        s += '%s. ' % publisher
    if link is not None:
        s += '%s. ' % link
    if doi is not None:
        s += 'Data set DOI: %s ' % doi
    if pubdate is not None:
        s += '(published on %s)' % pubdate
    
    citation = s.strip()

    ### BIBLIOGRAPHICCITATION ###
    # Construct a standardized bibliographic citation following the formula from the 
    # VertNet norms.
    bib = '%s. %s' % (bestid, citation)

    d = {}
    d['keyname'] = keyname
    d['references'] = references
    d['citation'] = citation
    d['bibliographiccitation'] = bib
    d['basisofrecord'] = basisofrecord
    d['dctype'] = dctype
    return d

def license_resolution(rec):
    """ Create a dictionary of completed, corrected license fields from data in 
        a dictionary.
    parameters:
        rec - dictionary to search for georeference input (required)
    returns:
        dictionary of completed, corrected georeference fields
    """
    license = None
    iptlicense = None
    haslicense = None
    if rec.has_key('license') == False or len(rec['license']) == 0:
        if rec.has_key('iptlicense') and len(rec['iptlicense']) > 0:
            iptlicense = rec['iptlicense']
            license = iptlicense
    else:
        license = rec['license']
    if license is not None:
        haslicense = 1
    else:
        haslicense = 0
    d = {}
    d['license'] = license
    d['iptlicense'] = iptlicense
    d['haslicense'] = haslicense
    return d

def dynamicproperties_resolution(rec):
    """ Create a clean version of the dynamicproperties in a dictionary.
    parameters:
        rec - dictionary to search for dynamicproperties (required)
    returns:
        cleaned version of dynamicproperties
    """
    if rec.has_key('dynamicproperties') == False or len(rec['dynamicproperties']) == 0:
        return None
    c = rec['dynamicproperties'].replace('"{','{').replace('}"','}').replace('""','"')
    return c

def occurrence_resolution(rec):
    """ Create a clean version of the occurrence fields in a dictionary. Depends on
        rec['wascaptive'] having been populated.
    parameters:
        rec - dictionary to search for occurrence fields (required)
    returns:
        cleaned version of occurrence fields
    """
    occremarks = None
    emeans = None
    if rec.has_key('occurrenceremarks') and len(rec['occurrenceremarks']) > 0:
        occremarks = strip_quote(rec['occurrenceremarks'])

    if rec.has_key('wascaptive') and rec['wascaptive'] == 1:
        emeans = 'managed'
    
    d = {}
    d['occurrenceremarks'] = occremarks
    d['establishmentmeans'] = emeans
    return d

def location_resolution(rec):
    """ Create a clean version of the location fields in a dictionary.
    parameters:
        rec - dictionary to search for location fields (required)
    returns:
        cleaned version of location fields
    """
    loc = None
    locremarks = None
    if rec.has_key('locality') and len(rec['locality']) > 0:
        loc = strip_quote(rec['locality'])
    if rec.has_key('locationremarks') and len(rec['locationremarks']) > 0:
        locremarks = strip_quote(rec['locationremarks'])
    d = {}
    d['locality'] = loc
    d['locationremarks'] = locremarks
    return d

def georef_resolution(rec): 
    """ Create a dictionary of completed, corrected georeference fields from data in 
        a dictionary.
    parameters:
        rec - dictionary to search for georeference input (required)
    returns:
        dictionary of completed, corrected georeference fields
    """
    lat = None
    lng = None
    datum = None
    unc = None
    gdate = None
    gsources = None
    if rec.has_key('decimallatitude') and rec.has_key('decimallongitude'):
        if valid_latlng(rec['decimallatitude'], rec['decimallongitude']):
            lat = rec['decimallatitude']
            lng = rec['decimallongitude']
            if rec.has_key('geodeticdatum') and len(rec['geodeticdatum']) > 0:
                datum = rec['geodeticdatum']
            else:
                datum = 'not recorded'
            if rec.has_key('coordinateuncertaintyinmeters'):
                unc = _coordinateuncertaintyinmeters(rec['coordinateuncertaintyinmeters'])
            # Try to clean dateidentified
            if rec.has_key('georeferenceddate') and len(rec['georeferenceddate']) > 0:
                gdate = rec['georeferenceddate'].strip(' 00:00:00.0').strip(' 0:00:00')
                cleandate = w3c_datestring(gdate)
                if cleandate is not None:
                    gdate = cleandate
            if rec.has_key('georeferencesources') and len(rec['georeferencesources']) > 0:
                gsources = rec['georeferencesources'].replace('""','"').replace('""','"')
    d = {}
    d['decimallatitude'] = lat
    d['decimallongitude'] = lng
    d['coordinateuncertaintyinmeters'] = unc
    d['geodeticdatum'] = datum
    d['georeferenceddate'] = gdate
    d['georeferencesources'] = gsources
    return d

def event_resolution(rec):
    """ Create a dictionary of completed, corrected event fields from data in 
        a dictionary.
    parameters:
        rec - dictionary to search for event input (required)
    returns:
        dictionary of completed, corrected event fields
    """
    year = None
    month = None
    day = None
    begindate = None
    beginyear = None
    beginmonth = None
    beginday = None
    enddate = None
    endyear = None
    endmonth = None
    endday = None
    begindayofyear = None
    enddayofyear = None
    isoeventdate = None
    verbatimeventdate = None
    eventremarks = None

    if rec.has_key('year') and len(str(rec['year']).strip())>0:
        year = rec['year']
    if rec.has_key('month') and len(str(rec['month']).strip())>0:
        month = rec['month']
    if rec.has_key('day') and len(str(rec['day']).strip())>0:
        day = rec['day']

    if rec.has_key('verbatimeventdate') and len(rec['verbatimeventdate'].strip())>0:
        if rec.has_key('eventdate') == False or len(rec['eventdate'].strip())==0:
            rec['eventdate'] = rec['verbatimeventdate']

    if rec.has_key('eventdate') and len(rec['eventdate'].strip())>0:
        ed = rec['eventdate']
        # Set the verbatimeventdate from event date if verbatimeventdate is empty
        if rec.has_key('verbatimeventdate') and len(rec['verbatimeventdate']) > 0:
            verbatimeventdate = rec['verbatimeventdate']
        else:
            verbatimeventdate = ed
        # Get begin and end dates from eventdate
        ds = ed.replace('//','/').split('/')
        if len(ds) == 1:
            begindate = ds[0]
            if len(ds) > 1:
                enddate = ds[1]
            else:
                enddate = begindate
        else:
            begindate = ed
            enddate = ed

    # Try to clean begin date
    cleaned = w3c_datestring(begindate)
    if cleaned is not None:
        begindate = cleaned
    # Try to clean end date
    cleaned = w3c_datestring(enddate)
    if cleaned is not None:
        enddate = cleaned

    # If there still is no begin date, try to get it from year, month, day
    if begindate is None:
         begindate = iso_datestring_from_ymd(year, month, day)
    if enddate is None:
         enddate = begindate

    beginyear, beginmonth, beginday = ymd_from_iso_datestring(begindate)
    endyear, endmonth, endday = ymd_from_iso_datestring(enddate)

    # Set the year, month, and day if they are not already populated and can be 
    # unambiguously determined.
    if year is None and beginyear == endyear:
        year = beginyear
    if month is None and beginmonth == endmonth:
        month = beginmonth
    if day is None and beginday == endday:
        day = beginday

    # Set the begin and end days of year from begin and end dates
    begindayofyear = day_of_year(begindate)
    if begindate == enddate:
        enddayofyear = begindayofyear
    else:
        enddayofyear = day_of_year(enddate)

    # Set the isodate from the begin and end dates
    if begindate is None:
        begindate = ''
    if enddate is None:
        enddate = ''
    if begindate == enddate:
        isodate = begindate
    else:
        isodate = '%s/%s' % (begindate, enddate)
    if isodate == '/' or isodate == '':
        isodate = None

    if rec.has_key('eventremarks') and len(rec['eventremarks']) > 0:
        eventremarks = rec['eventremarks'].replace('""','"').replace('""','"')

    d = {}
    d['year'] = year
    d['month'] = month
    d['day'] = day
    d['startdayofyear'] = begindayofyear
    d['enddayofyear'] = enddayofyear
    d['eventdate'] = isodate
    d['verbatimeventdate'] = verbatimeventdate
    d['eventremarks'] = eventremarks
    return d

def identification_resolution(rec):
    """ Create a clean version of the identification fields in a dictionary.
    parameters:
        rec - dictionary to search for identification fields (required)
    returns:
        cleaned version of identification fields
    """
    previds = None
    idrefs = None
    idremarks = None
    typestatus = None
    iddate = None
    if rec.has_key('previousidentifications') and len(rec['previousidentifications']) > 0:
        previds = strip_quote(rec['previousidentifications'])
    if rec.has_key('identificationreferences') and \
       len(rec['identificationreferences']) > 0:
        idrefs = strip_quote(rec['identificationreferences'])
    if rec.has_key('identificationremarks') and len(rec['identificationremarks']) > 0:
        idremarks = strip_quote(rec['identificationremarks'])
    if rec.has_key('typestatus') and len(rec['typestatus']) > 0:
        typestatus = strip_quote(rec['typestatus'])

    # Try to clean dateidentified
    if rec.has_key('dateidentified') and len(rec['dateidentified']) > 0:
        iddate = w3c_datestring(rec['dateidentified'])
        if iddate is None:
            iddate = rec['dateidentified']

    d = {}
    d['previousidentifications'] = previds
    d['identificationreferences'] = idrefs
    d['identificationremarks'] = idremarks
    d['dateidentified'] = iddate
    d['typestatus'] = typestatus
    return d

def strip_quote(str): 
    """ Remove excessive quoting.
    parameters:
        str - string (required)
    returns:
        string with the excessive quoting removed
    """
    try:
        return str.replace('""','"').replace('""','"')
    except:
        return None

def as_float(str): 
    """ Convert a string into a float, if possible.
    parameters:
        str - string (required)
    returns:
        a float equivalent of the string, or None
    """
    try:
        return float(str)
    except:
        return None

def as_int(str): 
    """ Convert a string into an int, if possible.
    parameters:
        str - string (required)
    returns:
        an int equivalent of the string, or None
    """
    try:
        return int(str)
    except:
        return None

def valid_year(year): 
    """ Determine if a value can be interpreted as a year.
    parameters:
        year - string, int or float (required)
    returns:
        True if the value can be interpreted as a valid year, otherwise False
    """
    fyear = as_int(year)
    if fyear is None:
        return False
    if fyear < 1:
        return False
    if fyear > datetime.now().year:
        return False
    return True
 
def valid_month(month): 
    """ Determine if a value can be interpreted as a month.
    parameters:
        month - string, int or float (required)
    returns:
        True if the value can be interpreted as a valid month, otherwise False
    """
    fmonth = as_int(month)
    if fmonth is None:
        return False
    if fmonth < 1:
        return False
    if fmonth > 12:
        return False
    return True

def valid_day(day, month=None, year=None): 
    """ Determine if a value can be interpreted as a valid day of a month.
    parameters:
        day - string, int or float (required)
        month - string, int or float (optional)
        year - string, int or float (optional)
    returns:
        True if the value can be interpreted as a valid day in the given month
        and year, otherwise False
    """
    fday = as_int(day)
    if fday is None:
        return False
    if fday < 1:
        return False
    if fday > 31:
        return False
    # now look at month dependencies
    fmonth = as_int(month)
    if fmonth is None:
        return True
    if fmonth in (1,3,5,7,8,10,12):
        return True
    if fday > 30:
        return False
    if fmonth in (4,6,9,11):
        return True
    if fday < 29:
        return True
    if fday == 30:
        return False
    fyear = as_int(year)
    if fyear is None:
        return True
    if leap(year) == 1:
        return True
    return False

def leap(year): 
    """ Determine if the year is a leap year.
    parameters:
        year - string, int or float (required)
    returns:
        True if the value can be interpreted as a valid leap year, otherwise False
    """
    leap = 0
    fyear = as_int(year)
    if fyear is None:
        return 0
    if fyear < 1582:
        return 0
    # If the year is evenly divisible by 4
    if fyear % 4 == 0:
        # If the year is a century year
        if fyear % 100 == 0:
            # If the century year is evenly divisible by 400
            if fyear % 400 == 0:
                leap = 1
        else:
            leap = 1
    return leap

def day_of_year(datestring): 
    """ Determine the day of the year from a W3C date string.
    parameters:
        datestring - string (required)
    returns:
        an integer for the ordinal day of the year matching the given date, or None.
    """
    try:
       y, m, d = datestring.split('-')
    except:
       return None
    if y is None or m is None or d is None:
        return None
    if valid_year(y):
        year = as_int(y)
        if year is None:
            return None
    else:
        return None
    if valid_month(m):
        month = as_int(m)
        if month is None:
            return None
    else:
        return None
    if valid_day(d, m, y):
        day = as_int(d)
        if day is None:
            return None
    else:
        return None
    dayofyearforfirst = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    doy = dayofyearforfirst[month-1] + day
    if month >2 and leap(year):
        doy += 1
    return doy

def iso_datestring_from_ymd(year, month, day): 
    """ Construct an ISO8601 date string from year, month and day.
    parameters:
        year - int, float or string (required)
        month - int, float or string (optional)
        day - int, float or string (optional)
    returns:
        a date in ISO8601 date format, or None.
    """
    if year is None or len(str(year)) == 0:
        # Can't make an ISO date without a year
        return None
    if valid_year(year) is False:
        # Shouldn't make an ISO date if the year is not valid
        return None
    hasmonth = valid_month(month)
    hasday = valid_day(day, month, year)
    isodate = str(year)
    if hasmonth == True:
        m = as_int(month)
        if m is not None:
            if m > 9:
                isodate += '-'+str(m)
            else:
                isodate += '-0'+str(m)
            if hasday == True:
                d = as_int(day)
                if d is not None:
                    if d > 9:
                        isodate += '-'+str(d)
                    else:
                        isodate += '-0'+str(d)
    return isodate

def ymd_from_iso_datestring(datestring): 
    """ Get the year, month and day from a string in W3C-formatted datetime (yyyy-mm-dd).
    parameters:
        datestring - string (required)
    returns:
        (year, month, day) - a tuple with the three derived values.
    """
    if datestring is None or len(datestring)==0:
        return (None, None, None)
    d = datestring.split('-')
    year = as_int(d[0])
    month = None
    day = None
    if len(d)>1:
        month = as_int(d[1])
    if len(d)>2:
        day = as_int(d[2])
    return (year, month, day)

def w3c_datestring(datestring): 
    """ Create a W3C date as a string given an input date as a string.
    parameters:
        datestring - string (required)
    returns:
        a W3C-formatted date string, or None
    """
    # Try date as YYYY-MM-DD or DD MMM YYYY
    d = format_date_as_w3c(['YYYY-M-D', 'D MMM YYYY'], datestring)
    if d is not None:
        return d
    # Try date as MM/DD/YYYY
    d = format_date_as_w3c(['D/M/YYYY'], datestring)
    # Try date as DD/MM/YYYY
    a = format_date_as_w3c(['M/D/YYYY'], datestring)
    if a is None:
        if d is not None:
            # Date fits DD/MM/YYYY only
            return d
        # Date doesn't fit either remaining format
        return None
    # Date matches MM/DD/YYYY
    if d is None:
        # Date fits MM/DD/YYYY only
        return a
    # Date matches both MM/DD/YYYY and DD/MM/YYYY
    if a==d:
        return a
    return None

def format_date_as_w3c(formats, datestring):
    """ Construct an W3C date string from a date string in one of the given formats.
    parameters:
        formats - a list of date formats to try (required)
        datestring - date to convert, as string (required)
    returns:
        a W3C-formatted date string, or None
    """
    try:
        d = arrow.get(datestring, formats).format('YYYY-MM-DD')
        return d
    except:
       return None

def valid_latlng(lat,lng): 
    """ Test the validity of lat and lng as geographic coordinates in decimal degrees.
    parameters:
        lat - latitude as numeric or string (required)
        lng - longitude as numeric or string (required)
    returns:
        True if valid otherwise False
    """
    flat = as_float(lat)
    if flat is None:
        return False
    if flat < -90 or flat > 90:
        return False
    flng = as_float(lng)
    if flng is None:
        return False
    if flng < -180 or flng > 180:
        return False
    if flat == 0 and flng == 0:
        return False
    return True

def valid_coords(rec): 
    """ Test the validity of the geographic coordinates in a dictionary.
    parameters:
        rec - dictionary to search for geographic coordinates 
              in decimal degrees (required)
    returns:
        True if decimallatitude and decimallongitude in rec are in valid ranges, 
        otherwise False
    """
    if rec is None:
        return False
    if rec.has_key('decimallatitude') == False:
        return False
    if rec.has_key('decimallongitude') == False:
        return False
    return valid_latlng(rec['decimallatitude'],rec['decimallongitude'])

def _coordinateuncertaintyinmeters(unc): 
    """ Round the value of unc up to an integer if it is a number greater than zero, 
        otherwise return None
    parameters:
        unc - the value to make into a valid coordinateuncertaintyinmeters (required)
    returns:
        the valid coordinateuncertaintyinmeters as an integer, or None
    """
    uncertaintyinmeters = as_float(unc)
    if uncertaintyinmeters is None:
        return None
    # Check to see if uncertaintyinmeters is less than one. Zero is not a legal 
    # value. Less than one is an error in concept.
    if uncertaintyinmeters < 1:
        return None
    # Return the nearest rounded up meter.
    i_unc = as_int(uncertaintyinmeters)
    if uncertaintyinmeters == i_unc:
        return i_unc
    return int( round(uncertaintyinmeters + 0.5) )

def valid_georef(rec): 
    """ Test the validity of the georeference in a dictionary.
    parameters:
        rec - dictionary to search for georeference (required)
    returns:
        True if georeference is complete and valid, otherwise False
    """
    # If any of the fields that make up a valid georeference are missing, return False
    if rec.has_key('coordinateuncertaintyinmeters') == False:
        return False
    if _coordinateuncertaintyinmeters(rec['coordinateuncertaintyinmeters']) is None:
        return False
    if rec.has_key('geodeticdatum') == False:
        return False
    if rec.has_key('decimallatitude') == False:
        return False
    if rec.has_key('decimallongitude') == False:
        return False
    # Otherwise, base validity on the validity of the coordinates and uncertainty
    unc = as_float(rec['coordinateuncertaintyinmeters'])
    if  unc < 1:
        return False
    valid = valid_latlng(rec['decimallatitude'],rec['decimallongitude'])
    return valid

def read_header(fullpath, dialect = None):
    """ Get the header line of a CSV or TXT data file.
    parameters:
        fullpath - full path to the input file (required)
        dialect - csv.dialect object with the attributes of the input file (default None)
    returns:
        header - a list containing the fields in the original header
    """
    if fullpath is None or len(fullpath)==0:
        logging.debug('No file given in read_header().')
        return None

    # Cannot function without an actual file where the full path points
    if os.path.isfile(fullpath) == False:
        logging.debug('File %s not found in read_header().' % fullpath)
        return None

    header = None

    # If no explicit dialect for the file is given, figure it out from the file
    if dialect is None:
        dialect = csv_file_dialect(fullpath)

    # Open up the file for processing
    with open(fullpath, 'rU') as csvfile:
        reader = csv.DictReader(csvfile, dialect=dialect)
        # header is the list as returned by the reader
        header=reader.fieldnames

    return header

def tsv_dialect(): 
    """ Get a dialect object with TSV properties.
    parameters:
        None
    returns:
        dialect - a csv.dialect object with TSV attributes"""
    dialect = csv.excel_tab
    dialect.lineterminator='\n'
    dialect.delimiter='\t'
    dialect.escapechar=''
    dialect.doublequote=True
    dialect.quotechar=''
    dialect.quoting=csv.QUOTE_NONE
    dialect.skipinitialspace=True
    dialect.strict=False
    return dialect

def csv_file_dialect(fullpath): 
    """ Detect the dialect of a CSV or TXT data file.
    parameters:
        fullpath - full path to the file to process (required)
    returns:
        dialect - a csv.dialect object with the detected attributes
    """
    if fullpath is None or len(fullpath) == 0:
        logging.debug('No file given in csv_file_dialect().')
        return False

    # Cannot function without an actual file where full path points
    if os.path.isfile(fullpath) == False:
        logging.debug('File %s not found in csv_file_dialect().' % fullpath)
        return None

    # Let's look at up to readto bytes from the file
    readto = 4096
    filesize = os.path.getsize(fullpath)

    if filesize < readto:
        readto = filesize

    with open(fullpath, 'rb') as file:
        # Try to read the specified part of the file
        try:
            buf = file.read(readto)
            s = 'csv_file_dialect()'
            s += ' buf:\n%s' % buf
            logging.debug(s)
            # Make a determination based on existence of tabs in the buffer, as the
            # Sniffer is not particularly good at detecting TSV file formats. So, if the
            # buffer has a tab in it, let's treat it as a TSV file 
            if buf.find('\t')>0:
                return tsv_dialect()
#            dialect = csv.Sniffer().sniff(file.read(readto))
            # Otherwise let's see what we can find invoking the Sniffer.
            dialect = csv.Sniffer().sniff(buf)
        except csv.Error:
            # Something went wrong, so let's try to read a few lines from the beginning of 
            # the file
            try:
                file.seek(0)
                s = 'csv_file_dialect()'
                s += ' Re-sniffing with tab to %s' % (readto)
                logging.debug(s)
                sample_text = ''.join(file.readline() for x in xrange(2,4,1))
                dialect = csv.Sniffer().sniff(sample_text)
            # Sorry, couldn't figure it out
            except csv.Error:
                logging.debug('Unable to determine csv dialect')
                return None
    
    # Fill in some standard values for the remaining dialect attributes        
    if dialect.escapechar is None:
        dialect.escapechar='/'

    dialect.skipinitialspace=True
    dialect.strict=False

    return dialect

def dialect_attributes(dialect):
    """ Show the attributes of a csv dialect.
    parameters:
        dialect - a csv.dialect object (required)
    returns:
        string showing the csv dialect attributes
    """
    if dialect is None:
        return 'No dialect given in dialect_attributes().'

    s = 'lineterminator: ' 

    if dialect.lineterminator == '\r':
        s+= '{CR}'
    elif dialect.lineterminator == '\n':
        s+= '{NL}'
    elif dialect.lineterminator == '\r\n':
        s+= '{CR}{NL}'
    else: 
        s += dialect.lineterminator

    s += '\ndelimiter: '

    if dialect.delimiter == '\t':
        s+= '{TAB}'
    else:
        s+= dialect.delimiter

    s += '\nescapechar: ' 
    s += dialect.escapechar

    s += '\ndoublequote: '

    if dialect.doublequote == True:
        s += 'True' 
    else:
        s += 'False' 

    s += '\nquotechar: ' 
    s += dialect.quotechar

    s += '\nquoting: ' 

    if dialect.quoting == csv.QUOTE_NONE:
        s += 'csv.QUOTE_NONE'
    elif dialect.quoting == csv.QUOTE_MINIMAL:
        s += 'csv.QUOTE_MINIMAL'
    elif dialect.quoting == csv.QUOTE_NONNUMERIC:
        s += 'csv.QUOTE_NONNUMERIC'
    elif dialect.quoting == csv.QUOTE_ALL:
        s += 'csv.QUOTE_ALL'

    s += '\nskipinitialspace: ' 

    if dialect.skipinitialspace == True:
        s += 'True'
    else:
        s += 'False'

    s += '\nstrict: ' 

    if dialect.strict == True:
        s += 'True'
    else:
        s += 'False'

    return s

def has_typestatus(rec):
    """ Check if dictionary has information in the typestatus field.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary contains information in 'typestatus', otherwise False.
    """
    if rec.has_key('typestatus') and rec['typestatus'] is not None and \
       len(rec['typestatus']) > 0:
        return 1
    return 0

def is_fossil(rec):
    """ Check if a record represents a fossil.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary represents a fossil, otherwise False.
    """
    if rec.has_key('basisofrecord'):
        if 'fossil' in rec['basisofrecord'].lower():
            return 1
    if rec.has_key('networks'):
        if 'paleo' in rec['networks'].lower():
            return 1
    return 0

def was_captive(rec):
    """ Check if a record has evidence that the organism was captive.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary has evidence that the organism was captive, 
        otherwise False.
    """
    f = 'establishmentmeans'
    if rec.has_key(f) and rec[f] is not None:
        if rec[f].lower() == 'native' or 'wild' in rec[f].lower():
            return 0
        if 'managed' in rec[f].lower():
          return 1
        if 'capt' in rec[f].lower():
          return 1
        if 'domestic' in rec[f].lower():
          return 1
    checkwords = ['captiv', 'aviary', 'lab born', 'aquarium']
    checkfields = ['locality', 'highergeography', 'occurrenceremarks', 'locationremarks',
        'eventremarks', 'fieldnotes', 'samplingprotocol']
    for f in checkfields:
        if rec.has_key(f) and rec[f] is not None:
            for w in checkwords:
                if w in rec[f].lower():
                    return 1
    # Check for fields that contain 'zoo', but not, for example, Kalamazoo or Zoology
    for f in checkfields:
        if rec.has_key(f) and rec[f] is not None:
            if 'zoo' in rec[f].lower():
                if 'azoo' not in rec[f].lower() and 'zool' not in rec[f].lower():
                    return 1
    return 0

def was_invasive(rec):
    """ Check if a record has evidence that the organism was invasive.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary has evidence that the organism was invasive, 
        otherwise False.
    """
    f = 'establishmentmeans'
    if rec.has_key(f) and rec[f] is not None:
        if rec[f].lower() == 'invasive':
            return 1
    return 0

tissuetokens = \
    ['+t', 'tiss', 'blood', 'dmso', 'dna', 'extract', 'froze', 'forzen',  'freez', 
     'heart', 'muscle', 'higado', 'kidney', 'liver', 'lung', 'nitrogen', 'pectoral', 
     'rinon', 'riñon', 'rnalater', 'sangre', 'toe', 'spleen', 'fin', 'ethanol', 
     'alcohol', 'etoh']

def has_tissue(rec):
    """ Check if a record has evidence of tissues viable for DNA extraction.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary contains evidence of tissues, otherwise False.
    """
    if rec.has_key('preparations') == False or len(rec['preparations']) == 0:
        return 0
    preps = rec['preparations'].lower()
    for token in tissuetokens:
        if token in preps:
            return 1
    return 0

def has_media(rec):
    """ Check if a record has evidence of associated media.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary contains evidence of media, otherwise False.
    """
    if rec.has_key('associatedmedia') and len(rec['associatedmedia']) > 0:
        return 1
    if rec.has_key('dctype') and len(rec['dctype']) > 0:
        if rec['dctype'].lower()=='sound':
            return 1
        if 'image' in rec['dctype'].lower():
            return 1
        return 0
    if rec.has_key('basisofrecord') and len(rec['basisofrecord']) > 0:
        if rec['basisofrecord'].lower()=='machineobservation':
            return 1
    return 0

def vn_type(rec):
    """ Characterize record as 'specimen', 'observation', or 'both' based on content of 
    the dctype and basisofrecord fields.
    parameters:
        rec - dictionary to search (required)
    returns:
        the basic type of record.
    """
    if rec.has_key('basisofrecord') == False or len(rec['basisofrecord']) == 0:
        if rec.has_key('dctype') == False or len(rec['dctype']) == 0:
            return 'indeterminate'
        elif 'object' in rec['dctype'].lower():
            return 'specimen'
        return 'observation'
    elif 'obs' in rec['basisofrecord'].lower():
        return 'observation'
    return 'specimen'

def has_binomial(rec):
    """ Check if a record has genus and specificepithet populated. Note that this does not 
       account for a scientificName that has a binomial and the genus is null.
    parameters:
        rec - dictionary to search (required)
    returns:
        True if the dictionary contains genus and specificepithet with content, 
        otherwise False.
    """
    if rec.has_key('genus') == False or len(rec['genus']) == 0:
        if rec.has_key('scientificname') and len(rec['scientificname'].split(' ')) > 1:
               return True
        return False
    if rec.has_key('specificepithet') == False or len(rec['specificepithet']) == 0:
        return False
    return True

def is_mappable(rec):
    """ Check if a record can be mapped.
    parameters:
        rec - dictionary to search (required)
    returns:
        1 if the dictionary contains valid coordinates, otherwise 0.
    """
    if valid_coords(rec) == True:
        return 1
    return 0

def rec_rank(rec):
    """ Rank the contents of the record for sorting purposes.
    parameters:
        rec - dictionary to search (required)
    returns:
        1 if the dictionary contains valid coordinates, otherwise 0.
    """
    if has_binomial(rec) is False:
        return 0
    # Must have a binomial to have a non-zero rank.
    rank = 0
    hasgeoref = valid_georef(rec)
    hascoords = False
    if hasgeoref == True:
        hascoords = True
    else:
        hascoords = valid_coords(rec)
    
    year = None
    month = None
    day = None
    if rec.has_key('year'):
        year = rec['year']
    if rec.has_key('month'):
        month = rec['month']
    if rec.has_key('day'):
        day = rec['day']
    hasyear = valid_year(year)
    hasmonth = valid_month(month)
    hasday = valid_day(day)

    if hasgeoref == True:
        rank = 9
        if hasyear == True:
            rank = 10
            if hasmonth == True:
                rank = 11
                if hasday == True:
                    rank = 12
    elif hascoords == True:
        rank = 5
        if hasyear == True:
            rank = 6
            if hasmonth == True:
                rank = 7
                if hasday == True:
                    rank = 8
    else:
        rank = 1
        if hasyear == True:
            rank = 2
            if hasmonth == True:
                rank = 3
                if hasday == True:
                    rank = 4
    return rank

class VNHarvestUtilsFramework():
    # testdatapath is the location of the files to test with
    testdatapath = './tests/data/'

    # following are files used as input during the tests, don't remove these
    tsvreadheaderfile = testdatapath + 'input_test_485_records.txt'

    # following are files output during the tests, remove these in dispose()
#    csvwriteheaderfile = testdatapath + 'test_write_header_file.csv'

    def dispose(self):
#        csvwriteheaderfile = self.csvwriteheaderfile
#        if os.path.isfile(csvwriteheaderfile):
#            os.remove(csvwriteheaderfile)
        return True

class VNHarvestUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.framework = VNHarvestUtilsFramework()

    def tearDown(self):
        self.framework.dispose()
        self.framework = None

    def test_source_files_exist(self):
        print 'testing source_files_exist'
        tsvreadheaderfile = self.framework.tsvreadheaderfile
        s = tsvreadheaderfile + ' does not exist'
        self.assertTrue(os.path.isfile(tsvreadheaderfile), s)

    def test_record_level_resolution(self):
        print 'testing record_level_resolution'
        rec={}
        b = record_level_resolution(rec)
        s = 'interpreted rec as having id when empty'
        self.assertIsNone(b, s)

        rec['icode'] = ''
        b = record_level_resolution(rec)
        s = 'interpreted rec as having id without an icode'
        self.assertIsNone(b, s)

        rec['icode'] = 'MVZ'
        b = record_level_resolution(rec)
        s = 'interpreted rec as having id without either a collectioncode '
        s += 'or a gbifdatasetid: %s' % rec
        self.assertIsNone(b, s)

        rec['gbifdatasetid'] = 'anything'
        b = record_level_resolution(rec)
        s = 'interpreted rec as having id without either a catalognumber '
        s += 'or an id: %s' % rec
        self.assertIsNone(b, s)

        rec={}
        rec['icode'] = 'MVZ'
        rec['collectioncode'] = 'Mamm'
        b = record_level_resolution(rec)
        s = 'interpreted rec as having id without either a catalognumber '
        s += 'or an id: %s' % rec
        self.assertIsNone(b, s)

        rec['catalognumber'] = '123'
        b = record_level_resolution(rec)
        s = 'incorrect interpretation of rec: %s interpretation: %s' % (rec, b)
        expected = 'mvz/mamm/123'
        self.assertEqual(b['keyname'], expected, s)
        expected = 'http://portal.vertnet.org/o/mvz/mamm?id=123'
        self.assertEqual(b['references'], expected, s)

        rec={}
        rec['icode'] = 'MVZ'
        rec['collectioncode'] = 'Mamm'
        rec['id'] = 'ANYthing'
        b = record_level_resolution(rec)
        s = 'incorrect interpretation of rec: %s interpretation: %s' % (rec, b)
        expected = 'mvz/mamm/anything'
        self.assertEqual(b['keyname'], expected, s)
        expected = 'http://portal.vertnet.org/o/mvz/mamm?id=anything'
        self.assertEqual(b['references'], expected, s)

        rec={}
        rec['icode'] = 'MVZ'
        rec['collectioncode'] = 'Mamm'
        rec['id'] = 'http://arctos.database.museum/guid/UAM:Herp:92?seid=497676'
        b = record_level_resolution(rec)
        s = 'incorrect interpretation of rec: %s interpretation: %s' % (rec, b)
        expected = 'mvz/mamm/http-arctos-database-museum-guid-uam-herp-92-seid-497676'
        self.assertEqual(b['keyname'], expected, s)
        expected = 'http://portal.vertnet.org/o/mvz/mamm?id='
        expected += 'http-arctos-database-museum-guid-uam-herp-92-seid-497676'
        self.assertEqual(b['references'], expected, s)

        rec['id'] = '123E4567-E89b-12D3-A456-426655440000'
        b = record_level_resolution(rec)
        s = 'incorrect interpretation of rec: %s interpretation: %s' % (rec, b)
        expected = 'mvz/mamm/123e4567-e89b-12d3-a456-426655440000'
        self.assertEqual(b['keyname'], expected, s)
        expected = 'http://portal.vertnet.org/o/mvz/mamm?id='
        expected += '123e4567-e89b-12d3-a456-426655440000'
        self.assertEqual(b['references'], expected, s)

        rec={}
        rec['icode'] = 'An iCode'
        rec['collectioncode'] = 'Collection Code'
        rec['catalognumber'] = 'ABC 123'
        b = record_level_resolution(rec)
        s = 'incorrect interpretation of rec: %s interpretation: %s' % (rec, b)
        expected = 'an-icode/collection-code/abc-123'
        self.assertEqual(b['keyname'], expected, s)
        expected = 'http://portal.vertnet.org/o/an-icode/collection-code?id=abc-123'
        self.assertEqual(b['references'], expected, s)

        rec={}
        rec['icode'] = 'A'
        rec['collectioncode'] = 'B'
        rec['catalognumber'] = 'C'
        rec['basisofrecord'] = 'specimen'
        f = 'basisofrecord'
        expected = 'PreservedSpecimen'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

#        rec['basisofrecord'] = 'PRESERVESPECIMEN'
        rec['basisofrecord'] = 'Preserved record'
        f = 'basisofrecord'
        expected = 'PreservedSpecimen'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['basisofrecord'] = 'PreservedSpecimen'
        f = 'basisofrecord'
        expected = 'PreservedSpecimen'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['basisofrecord'] = 'Material sample'
        f = 'basisofrecord'
        expected = 'MaterialSample'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['basisofrecord'] = 'Machine Observation'
        f = 'basisofrecord'
        expected = 'MachineObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Event'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['basisofrecord'] = 'MachineObservation'
        rec['dctype'] = 'PhysicalObject'
        f = 'basisofrecord'
        expected = 'MachineObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Event'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['basisofrecord'] = 'HumanObservation'
        rec['dctype'] = 'PhysicalObject'
        f = 'basisofrecord'
        expected = 'HumanObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Event'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec.pop('basisofrecord')
        rec['dctype'] = 'still'
        f = 'basisofrecord'
        expected = 'MachineObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'StillImage'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['dctype'] = 'moving'
        f = 'basisofrecord'
        expected = 'MachineObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'MovingImage'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['dctype'] = 'SOUND'
        f = 'basisofrecord'
        expected = 'MachineObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Sound'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec['dctype'] = 'object'
        f = 'basisofrecord'
        expected = 'Occurrence'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec.pop('dctype')
        rec['basisofrecord'] = 'Human observation'
#        rec['dctype'] = 'Event'
        f = 'basisofrecord'
        expected = 'HumanObservation'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Event'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec.pop('basisofrecord')
        f = 'basisofrecord'
        expected = 'Occurrence'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'Event'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

###
        rec['basisofrecord'] = 'FOSSIL'
        rec['isfossil']=is_fossil(rec)
        f = 'basisofrecord'
        expected = 'FossilSpecimen'
        b = record_level_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dctype'
        expected = 'PhysicalObject'
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (b[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

    def test_license_resolution(self):
        print 'testing license_resolution'
        rec={}
        b = license_resolution(rec)
        s = 'interpreted rec as having licenses when empty: %s' % b
        self.assertIsNone(b['license'], s)
        self.assertIsNone(b['iptlicense'], s)
        self.assertEquals(b['haslicense'], 0, s)

        rec['license'] = ''
        b = license_resolution(rec)
        s = 'interpreted rec as having licenses when empty: %s' % b
        self.assertIsNone(b['license'], s)
        self.assertIsNone(b['iptlicense'], s)
        self.assertEquals(b['haslicense'], 0, s)

        rec['license'] = 'CC0'
        b = license_resolution(rec)
        s = 'interpreted rec as not having license: %s' % rec
        self.assertEqual(b['license'], 'CC0', s)
        self.assertIsNone(b['iptlicense'], s)
        self.assertEquals(b['haslicense'], 1, s)

        rec={}
        rec['iptlicense'] = 'CC0'
        b = license_resolution(rec)
        s = 'interpreted rec as not having license: %s' % rec
        self.assertEqual(b['license'], 'CC0', s)
        self.assertEqual(b['iptlicense'], 'CC0', s)
        self.assertEquals(b['haslicense'], 1, s)

    def test_dynamicproperties_resolution(self):
        print 'testing dynamicproperties_resolution'
        rec={}
        b = dynamicproperties_resolution(rec)
        s = 'interpreted rec as having dynamicproperties when empty: %s' % b
        self.assertIsNone(b, s)

        f = 'dynamicproperties'
        rec[f] = ''
        b = dynamicproperties_resolution(rec)
        s = 'interpreted rec as having dynamicproperties when empty: %s' % b
        self.assertIsNone(b, s)

        rec[f] = '"{ ""key":"value"" }"'
        expected = '{ "key":"value" }'
        b = dynamicproperties_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b, expected, s)

    def test_occurrence_resolution(self):
        print 'testing occurrence_resolution'
        rec={}
        b = occurrence_resolution(rec)
        s = 'interpreted rec as having occurrence fields when empty: %s' % b
        self.assertIsNone(b['occurrenceremarks'], s)

        f = 'occurrenceremarks'
        rec[f] = 'a remark'
        expected = 'a remark'
        b = occurrence_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = 'a remark with """excessive""" double quotes'
        expected = 'a remark with "excessive" double quotes'
        b = occurrence_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

    def test_event_resolution(self):
        print 'testing event_resolution'
        rec={}
        b = event_resolution(rec)
        s = 'interpreted rec having event when empty: %s' % b
        self.assertIsNone(b['year'], s)
        self.assertIsNone(b['month'], s)
        self.assertIsNone(b['day'], s)
        self.assertIsNone(b['startdayofyear'], s)
        self.assertIsNone(b['enddayofyear'], s)
        self.assertIsNone(b['eventdate'], s)

        rec['year'] = 2000
        rec['month'] = 1
        rec['day'] = 1
        b = event_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['year'], 2000, s)
        self.assertEqual(b['month'], 1, s)
        self.assertEqual(b['day'], 1, s)
        self.assertEqual(b['startdayofyear'], 1, s)
        self.assertEqual(b['enddayofyear'], 1, s)
        self.assertEqual(b['eventdate'], '2000-01-01', s)

        rec={}
        rec['eventdate'] = '1/1/2000'
        b = event_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['year'], 2000, s)
        self.assertEqual(b['month'], 1, s)
        self.assertEqual(b['day'], 1, s)
        self.assertEqual(b['startdayofyear'], 1, s)
        self.assertEqual(b['enddayofyear'], 1, s)
        self.assertEqual(b['eventdate'], '2000-01-01', s)
        self.assertEqual(b['verbatimeventdate'], '1/1/2000', s)

        rec['eventdate'] = '11/15/2004'
        rec['eventremarks'] = 'test """double-quote"" reduction'
        b = event_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['year'], 2004, s)
        self.assertEqual(b['month'], 11, s)
        self.assertEqual(b['day'], 15, s)
        self.assertEqual(b['startdayofyear'], 320, s)
        self.assertEqual(b['enddayofyear'], 320, s)
        self.assertEqual(b['eventdate'], '2004-11-15', s)
        self.assertEqual(b['verbatimeventdate'], '11/15/2004', s)
        self.assertEqual(b['eventremarks'], 'test "double-quote" reduction', s)

        rec={}
        rec['verbatimeventdate'] = '8 Mar 2000'
        rec['year'] = ''
        rec['month'] = ''
        rec['day'] = ''
        rec['eventdate'] = ''
        b = event_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['year'], 2000, s)
        self.assertEqual(b['month'], 3, s)
        self.assertEqual(b['day'], 8, s)
        self.assertEqual(b['startdayofyear'], 68, s)
        self.assertEqual(b['enddayofyear'], 68, s)
        self.assertEqual(b['eventdate'], '2000-03-08', s)
        self.assertEqual(b['verbatimeventdate'], '8 Mar 2000', s)

    def test_location_resolution(self):
        print 'testing location_resolution'
        rec={}
        b = location_resolution(rec)
        s = 'interpreted rec as having location fields when empty: %s' % b
        self.assertIsNone(b['locality'], s)
        self.assertIsNone(b['locationremarks'], s)

        f = 'locationremarks'
        rec[f] = 'a remark'
        expected = 'a remark'
        b = location_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = 'Wonder where ""The Gap"" is.'
        expected = 'Wonder where "The Gap" is.'
        b = location_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b, expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

    def test_georef_resolution(self):
        print 'testing georef_resolution'
        rec={}
        b = georef_resolution(rec)
        s = 'interpreted rec having georeference when empty: %s' % b
        self.assertIsNone(b['decimallatitude'], s)
        self.assertIsNone(b['decimallongitude'], s)
        self.assertIsNone(b['geodeticdatum'], s)
        self.assertIsNone(b['coordinateuncertaintyinmeters'], s)
        self.assertIsNone(b['georeferenceddate'], s)
        self.assertIsNone(b['georeferencesources'], s)

        rec['decimallatitude'] = 1
        rec['decimallongitude'] = 1
        rec['geodeticdatum'] = 'WGS84'
        rec['coordinateuncertaintyinmeters'] = 1
        rec['georeferenceddate'] = '2016-07-07 00:00:00.0'
        rec['georeferencesources'] = '<a href=""http://maps.google.com"">'
        b = georef_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['decimallatitude'], 1, s)
        self.assertEqual(b['decimallongitude'], 1, s)
        self.assertEqual(b['geodeticdatum'], 'WGS84', s)
        self.assertEqual(b['coordinateuncertaintyinmeters'], 1, s)
        self.assertEqual(b['georeferenceddate'], '2016-07-07', s)
        self.assertEqual(b['georeferencesources'], '<a href="http://maps.google.com">', s)

        rec.pop('geodeticdatum')
        b = georef_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['decimallatitude'], 1, s)
        self.assertEqual(b['decimallongitude'], 1, s)
        self.assertEqual(b['geodeticdatum'], 'not recorded', s)
        self.assertEqual(b['coordinateuncertaintyinmeters'], 1, s)

        rec['decimallatitude'] = 1
        rec['coordinateuncertaintyinmeters'] = 0
        b = georef_resolution(rec)
        s = 'rec: %s incorrectly interpreted as %s' % (rec, b)
        self.assertEqual(b['decimallatitude'], 1, s)
        self.assertEqual(b['decimallongitude'], 1, s)
        self.assertEqual(b['geodeticdatum'], 'not recorded', s)
        self.assertIsNone(b['coordinateuncertaintyinmeters'], s)

        f = 'georeferenceddate'
        rec[f] = '8 Jul 2016'
        expected = '2016-07-08'
        b = georef_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '2016'
        expected = '2016'
        b = georef_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '2016-07-08 00:00:00.0'
        expected = '2016-07-08'
        b = georef_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

    def test_identification_resolution(self):
        print 'testing identification_resolution'
        rec={}
        b = identification_resolution(rec)
        s = 'interpreted rec as having identification fields when empty: %s' % b
        self.assertIsNone(b['previousidentifications'], s)
        self.assertIsNone(b['identificationreferences'], s)
        self.assertIsNone(b['identificationremarks'], s)
        self.assertIsNone(b['typestatus'], s)

        f = 'previousidentifications'
        rec[f] = 'old id'
        expected = 'old id'
        b = identification_resolution(rec)
        s = '\nwas: %s\nexp: %s\n' % (b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '"an ""old id"""'
        expected = '"an "old id"'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'identificationreferences'
        rec[f] = '<a href=""aurl.org"">'
        expected = '<a href="aurl.org">'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '<a href="aurl.org">'
        expected = '<a href="aurl.org">'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'identificationremarks'
        rec[f] = '"This is found ""in remarks"""'
        expected = '"This is found "in remarks"'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '"This is found "in remarks""'
        expected = '"This is found "in remarks"'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'typestatus'
        rec[f] = 'holotype'
        expected = 'holotype'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = 'holotype of <a href=""http://someref.org"">'
        expected = 'holotype of <a href="http://someref.org">'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        f = 'dateidentified'
        rec[f] = '8 Jul 2016'
        expected = '2016-07-08'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '2016'
        expected = '2016'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

        rec[f] = '2016-07-08 00:00:00.0'
        expected = '2016-07-08'
        b = identification_resolution(rec)
        s = '\nwas: %s\ngot: %s\nexp: %s\n' % (rec[f], b[f], expected)
        s += '%s not as expected' % f
        self.assertEqual(b[f], expected, s)

    def test_as_float(self):
        print 'testing as_float'
        a = '0'
        expected = 0
        b = as_float(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))
        
        a = 1
        expected = 1
        b = as_float(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))
        
        a = '01'
        expected = 1
        b = as_float(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = '-2'
        expected = -2
        b = as_float(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = '.12345678'
        expected = 0.12345678
        b = as_float(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = 'a'
        expected = None
        b = as_float(a)
        self.assertIsNone(b, '%s not a float' % a)

        a = None
        expected = None
        b = as_float(a)
        self.assertIsNone(b, '%s not a float' % a)

    def test_as_int(self):
        print 'testing as_int'
        a = '0'
        expected = 0
        b = as_int(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))
        
        a = 1
        expected = 1
        b = as_int(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = '01'
        expected = 1
        b = as_int(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = '-2'
        expected = -2
        b = as_int(a)
        self.assertEqual(b, expected,
            '%s not equal to %s' % (b, expected))

        a = '.12345678'
        expected = None
        b = as_int(a)
        self.assertIsNone(b, '%s not a int' % a)

        a = 'a'
        expected = None
        b = as_int(a)
        self.assertIsNone(b, '%s not a int' % a)

    def test_iso_datestring_from_ymd(self):
        print 'testing iso_datestring_from_ymd'
        year = '2016'
        month = None
        day = None
        expected = '2016'
        b = iso_datestring_from_ymd(year, month, day)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)
        
        year = 2016
        month = None
        day = None
        expected = '2016'
        b = iso_datestring_from_ymd(year, month, day)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = '999'
        month = None
        day = None
        expected = '999'
        b = iso_datestring_from_ymd(year, month, day)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)
        
        year = 'YYYY'
        month = None
        day = None
        b = iso_datestring_from_ymd(year, month, day)
        s = 'Date found from %s' % year
        self.assertIsNone(b, '%s cannot be converted to a date string' % year)
        
        year = '1000'
        month = '1'
        day = None
        expected = '1000-01'
        b = iso_datestring_from_ymd(year, month, day)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = '1963'
        month = '13'
        day = None
        b = iso_datestring_from_ymd(year, month, day)
        expected = '1963'
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = '1963'
        month = '3'
        day = None
        b = iso_datestring_from_ymd(year, month, day)
        expected = '1963-03'
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = '1963'
        month = 3
        day = '8'
        b = iso_datestring_from_ymd(year, month, day)
        expected = '1963-03-08'
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = '1754'
        month = '12'
        day = '32'
        b = iso_datestring_from_ymd(year, month, day)
        expected = '1754-12'
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        year = 1865
        month = '11'
        day = '31'
        b = iso_datestring_from_ymd(year, month, day)
        expected = '1865-11'
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

    def test_valid_day(self):
        print 'testing valid_day'
        day = '32'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = '0'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 0
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = '-1'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 'a'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 1
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = '1'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = 28
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = '28'
        month = None
        year = None
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = 31
        month = 4
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 30
        month = 2
        year = None
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 29
        month = 2
        year = None
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = 29
        month = 2
        year = 2004
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = 29
        month = 2
        year = 2000
        b = valid_day(day, month, year)
        s = '%s should be a valid day for month: %s year: %s' % (day, month, year)
        self.assertTrue(b, s)

        day = 29
        month = 2
        year = 2001
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

        day = 29
        month = 2
        year = 1900
        b = valid_day(day, month, year)
        s = '%s should not be a valid day for month: %s year: %s' % (day, month, year)
        self.assertFalse(b, s)

    def test_valid_month(self):
        print 'testing valid_month'
        month = None
        b = valid_month(month)
        s = '%s should not be a valid month' % (month)
        self.assertFalse(b, s)

        month = '0'
        b = valid_month(month)
        s = '%s should not be a valid month' % (month)
        self.assertFalse(b, s)

        month = 0
        b = valid_month(month)
        s = '%s should not be a valid month' % (month)
        self.assertFalse(b, s)

        month = '13'
        b = valid_month(month)
        s = '%s should not be a valid month' % (month)
        self.assertFalse(b, s)

        month = 13
        b = valid_month(month)
        s = '%s should not be a valid month' % (month)
        self.assertFalse(b, s)

        month = '1'
        b = valid_month(month)
        s = '%s should be a valid month' % (month)
        self.assertTrue(b, s)

        month = 1
        b = valid_month(month)
        s = '%s should be a valid month' % (month)
        self.assertTrue(b, s)

        month = '12'
        b = valid_month(month)
        s = '%s should be a valid month' % (month)
        self.assertTrue(b, s)

        month = 12
        b = valid_month(month)
        s = '%s should be a valid month' % (month)
        self.assertTrue(b, s)

    def test_valid_year(self):
        print 'testing valid_year'
        year = None
        b = valid_year(year)
        s = '%s should not be a valid year' % (year)
        self.assertFalse(b, s)

        year = '0'
        b = valid_year(year)
        s = '%s should not be a valid year' % (year)
        self.assertFalse(b, s)

        year = 0
        b = valid_year(year)
        s = '%s should not be a valid year' % (year)
        self.assertFalse(b, s)

        year = '999'
        b = valid_year(year)
        s = '%s should be a valid year' % (year)
        self.assertTrue(b, s)

        year = 999
        b = valid_year(year)
        s = '%s should be a valid year' % (year)
        self.assertTrue(b, s)

        year = '1000'
        b = valid_year(year)
        s = '%s should be a valid year' % (year)
        self.assertTrue(b, s)

        year = 1000
        b = valid_year(year)
        s = '%s should be a valid year' % (year)
        self.assertTrue(b, s)

        year = datetime.now().year
        b = valid_year(year)
        s = '%s should be a valid year' % (year)
        self.assertTrue(b, s)

        year += 1
        b = valid_year(year)
        s = '%s should not be a valid year' % (year)
        self.assertFalse(b, s)

    def test_day_of_year(self):
        print 'testing day_of_year'
        adate = None
        b = day_of_year(adate)
        s = 'Day of year found without date'
        self.assertIsNone(b, s)

        adate = 2016
        b = day_of_year(adate)
        s = 'Day of year found with year only'
        self.assertIsNone(b, s)

        adate = '2003-12'
        b = day_of_year(adate)
        s = 'Day of year found with year and month only'
        self.assertIsNone(b, s)

        adate = '2003-10-32'
        b = day_of_year(adate)
        s = 'Day of year found with invalid date'
        self.assertIsNone(b, s)

        adate = '2003-14-12'
        b = day_of_year(adate)
        s = 'Day of year found with invalid date'
        self.assertIsNone(b, s)

        adate = '2016-1-1'
        b = day_of_year(adate)
        expected = 1
        s = 'the day of year for %s  should be %s, found %s' % (adate, expected, b)
        self.assertEqual(b, expected, s)

        adate = '2016-1-1'
        b = day_of_year(adate)
        expected = 1
        s = 'the day of year for %s should be %s, found %s' % (adate, expected, b)
        self.assertEqual(b, expected, s)

        adate = '2016-2-1'
        b = day_of_year(adate)
        expected = 32
        s = 'the day of year for %s should be %s, found %s' % (adate, expected, b)
        self.assertEqual(b, expected, s)

        adate = '2016-03-08'
        b = day_of_year(adate)
        expected = 68
        s = 'the day of year for %s should be %s, found %s' % (adate, expected, b)
        self.assertEqual(b, expected, s)

        adate = '2000-12-31'
        b = day_of_year(adate)
        expected = 366
        s = 'the day of year for %s should be %s, found %s' % (adate, expected, b)
        self.assertEqual(b, expected, s)

    def test_leap(self):
        print 'testing leap'
        year = None
        b = leap(year)
        expected = 0
        s = 'year %s should not be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = 0
        b = leap(year)
        expected = 0
        s = 'year %s should not be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = 1581
        b = leap(year)
        expected = 0
        s = 'year %s should not be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = 1584
        b = leap(year)
        expected = 1
        s = 'year %s should be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = 1900
        b = leap(year)
        expected = 0
        s = 'year %s should not be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = 2001
        b = leap(year)
        expected = 0
        s = 'year %s should not be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = '2000'
        b = leap(year)
        expected = 1
        s = 'year %s should be a leap year' % (year)
        self.assertEqual(b, expected, s)

        year = '2016'
        b = leap(year)
        expected = 1
        s = 'year %s should be a leap year' % (year)
        self.assertEqual(b, expected, s)

    def test_ymd_from_iso_datestring(self):
        print 'testing ymd_from_iso_datestring'
        a = '2016-06-28'
        expected = (2016, 6, 28)
        b = ymd_from_iso_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

    def test_w3c_datestring(self):
        print 'testing w3c_datestring'
        a = '2016-06-28'
        expected = '2016-06-28'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '2016-1-1'
        expected = '2016-01-01'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '1/1/2016'
        expected = '2016-01-01'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '21/1/2016'
        expected = '2016-01-21'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '1/13/2016'
        expected = '2016-01-13'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '11 Dec 1967'
        expected = '1967-12-11'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '1/1/2000'
        expected = '2000-01-01'
        b = w3c_datestring(a)
        s = '%s not equal to %s' % (b, expected)
        self.assertEqual(b, expected, s)

        a = '11 Dec 67'
        b = w3c_datestring(a)
        s = '%s interpreted incorrectly as unambiguous date' % a
        self.assertIsNone(b, s)

        a = '1/2/1867'
        b = w3c_datestring(a)
        s = '%s interpreted incorrectly as unambiguous date' % a
        self.assertIsNone(b, s)

        a = '12/11/1867'
        b = w3c_datestring(a)
        s = '%s interpreted incorrectly as unambiguous date' % a
        self.assertIsNone(b, s)

        a = '1999'
        b = w3c_datestring(a)
        s = '%s interpreted incorrectly as unambiguous date' % a
        self.assertIsNone(b, s)

    def test_valid_latlng(self):
        print 'testing valid_latlng'
        lat = '0'
        lng = 0
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as valid' % (lat, lng)
        self.assertFalse(b, s)

        lat = '0'
        lng = '0'
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as valid' % (lat, lng)
        self.assertFalse(b, s)

        lat = 0
        lng = 0
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as valid' % (lat, lng)
        self.assertFalse(b, s)

        lat = 91
        lng = 1
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as valid' % (lat, lng)
        self.assertFalse(b, s)

        lat = 1
        lng = 181
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as valid' % (lat, lng)
        self.assertFalse(b, s)

        lat = 90
        lng = 180
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as invalid' % (lat, lng)
        self.assertTrue(b, s)

        lat = '-90'
        lng = '-180'
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as invalid' % (lat, lng)
        self.assertTrue(b, s)

        lat = 0
        lng = -180
        b = valid_latlng(lat, lng)
        s = 'lat: %s lng: %s incorrectly interpreted as invalid' % (lat, lng)
        self.assertTrue(b, s)

    def test_valid_coords(self):
        print 'testing valid_coords and is_mappable'
        rec={}
        b = valid_coords(rec)
        s = 'interpreted rec having valid coords when empty'
        self.assertFalse(b, s)

        b = is_mappable(rec)
        s = 'interpreted rec as mappable when empty'
        self.assertFalse(b, s)

        rec['decimallatitude'] = 0
        b = valid_coords(rec)
        s = 'rec: %s incorrectly interpreted as having valid coordinates' % rec
        self.assertFalse(b, s)

        b = is_mappable(rec)
        s = 'rec: %s incorrectly interpreted as mappable' % rec
        self.assertFalse(b, s)

        rec['decimallongitude'] = 0
        b = valid_coords(rec)
        s = 'rec: %s incorrectly interpreted as having valid coordinates' % rec
        self.assertFalse(b, s)

        b = is_mappable(rec)
        s = 'rec: %s incorrectly interpreted as mappable' % rec
        self.assertFalse(b, s)

        b = is_mappable(rec)
        s = 'rec: %s incorrectly interpreted as mappable' % rec
        self.assertFalse(b, s)

        rec['decimallongitude'] = 90
        b = valid_coords(rec)
        s = 'rec: %s incorrectly interpreted as having invalid coordinates' % rec
        self.assertTrue(b, s)

        b = is_mappable(rec)
        s = 'rec: %s incorrectly interpreted as unmappable' % rec
        self.assertTrue(b, s)

        rec={}
        rec['decimallongitude'] = 90
        b = valid_coords(rec)
        s = 'rec: %s incorrectly interpreted as having valid coordinates' % rec
        self.assertFalse(b, s)

        b = is_mappable(rec)
        s = 'rec: %s incorrectly interpreted as mappable' % rec
        self.assertFalse(b, s)

    def test__coordinateuncertaintyinmeters(self):
        print 'testing _coordinateuncertaintyinmeters'
        unc = None
        b = _coordinateuncertaintyinmeters(unc)
        s = 'interpreted uncertainty as valid when empty'
        self.assertIsNone(b, s)

        unc = '0'
        b = _coordinateuncertaintyinmeters(unc)
        s = 'interpreted uncertainty (%s) as valid' % unc
        self.assertIsNone(b, s)

        unc = 0
        b = _coordinateuncertaintyinmeters(unc)
        s = 'interpreted uncertainty (%s) as valid' % unc
        self.assertIsNone(b, s)

        unc = -1
        b = _coordinateuncertaintyinmeters(unc)
        s = 'interpreted uncertainty (%s) as valid' % unc
        self.assertIsNone(b, s)

        unc = '1609.34'
        b = _coordinateuncertaintyinmeters(unc)
        expected = 1610
        s = '%s interpreted as expected (%s)' % (unc, b)
        self.assertEqual(b, expected, s)

    def test_valid_georef(self):
        print 'testing valid_georef'
        rec={}
        b = valid_georef(rec)
        s = 'interpreted rec having valid georeference when empty'
        self.assertFalse(b, s)

        rec['decimallatitude'] = 1
        rec['decimallongitude'] = 1
        rec['geodeticdatum'] = 'WGS84'
        rec['coordinateuncertaintyinmeters'] = 1
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as invalid' % rec
        self.assertTrue(b, s)

        rec['coordinateuncertaintyinmeters'] = 0
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as valid' % rec
        self.assertFalse(b, s)

        rec['coordinateuncertaintyinmeters'] = 1
        rec.pop('geodeticdatum')
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as valid' % rec
        self.assertFalse(b, s)

        rec['geodeticdatum'] = 'WGS84'
        rec.pop('coordinateuncertaintyinmeters')
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as valid' % rec
        self.assertFalse(b, s)

        rec['coordinateuncertaintyinmeters'] = 1
        rec.pop('decimallatitude')
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as valid' % rec
        self.assertFalse(b, s)

        rec['decimallatitude'] = 1
        rec.pop('decimallongitude')
        b = valid_georef(rec)
        s = 'rec: %s incorrectly interpreted as valid' % rec
        self.assertFalse(b, s)

    def test_tsv_dialect(self):
        print 'testing tsv_dialect'
        dialect = tsv_dialect()
#        s = dialect_attributes(dialect)
#        print s
        self.assertEqual(dialect.delimiter, '\t',
            'incorrect delimiter for tsv')
        self.assertEqual(dialect.lineterminator, '\n',
            'incorrect lineterminator for tsv')
        s = 'incorrect escapechar (%s) found for tsv ' % dialect.escapechar
        s += 'expected: %s' % ''
        self.assertEqual(dialect.escapechar, '', s)
        self.assertEqual(dialect.quotechar, '',
            'incorrect quotechar for tsv')
        self.assertTrue(dialect.doublequote,
            'doublequote not set to True for tsv')
        self.assertEqual(dialect.quoting, 3,
            'quoting not set to csv.QUOTE_NONE for tsv')
        self.assertTrue(dialect.skipinitialspace,
            'skipinitialspace not set to True for tsv')
        self.assertFalse(dialect.strict,
            'strict not set to False for tsv')

    def test_csv_file_dialect(self):
        print 'testing csv_file_dialect'
        tsvreadheaderfile = self.framework.tsvreadheaderfile
        dialect = csv_file_dialect(tsvreadheaderfile)
#        print 'dialect:\n%s' % dialect_attributes(dialect)
        self.assertIsNotNone(dialect, 'unable to detect tsv file dialect')
        self.assertEqual(dialect.delimiter, '\t',
            'incorrect delimiter detected for csv file')
        self.assertEqual(dialect.lineterminator, '\n',
            'incorrect lineterminator for csv file')
#        self.assertEqual(dialect.escapechar, '/',
#            'incorrect escapechar for csv file')
        s = 'incorrect escapechar (%s) found for csv ' % dialect.escapechar
        s += 'expected: %s' % ''
        self.assertEqual(dialect.escapechar, '', s)
        s = 'incorrect quotechar (%s) found for csv ' % dialect.quotechar
        s += 'expected: %s' % ''
        self.assertEqual(dialect.quotechar, '', s) 
        self.assertTrue(dialect.doublequote,
            'doublequote not set to False for csv file')
        self.assertEqual(dialect.quoting, csv.QUOTE_NONE,
            'quoting not set to csv.QUOTE_NONE for csv file')
        self.assertTrue(dialect.skipinitialspace,
            'skipinitialspace not set to True for csv file')
        self.assertFalse(dialect.strict,
            'strict not set to False for csv file')

    def test_read_header(self):
        print 'testing read_header'
        tsvreadheaderfile = self.framework.tsvreadheaderfile
        header = read_header(tsvreadheaderfile)
        modelheader = []
        modelheader.append('icode')
        modelheader.append('title')
        modelheader.append('citation')
        modelheader.append('contact')
#        ...
        modelheader.append('taxonomicstatus')
        modelheader.append('nomenclaturalstatus')
        modelheader.append('taxonremarks')

#        print 'len(header)=%s len(model)=%s\nheader:\nmodel:\n%s\n%s' \
#            % (len(header), len(modelheader), header, modelheader)
        d = len(header)
        self.assertEqual(d, 185, 'incorrect number of fields in header (%s)' % d	)
#        self.assertEqual(header, modelheader, 'header not equal to the model header')

    def test_is_fossil(self):
        print 'testing is_fossil'
        rec={}
        b = is_fossil(rec)
        s = 'interpreted rec as fossil when rec is empty'
        self.assertFalse(b, s)

        rec['basisofrecord'] = 'FossilSpecimen'
        b = is_fossil(rec)
        s = 'did not interpret %s as fossil' % rec['basisofrecord']
        self.assertTrue(b, s)
        
        rec['basisofrecord'] = 'PreservedSpecimen'
        b = is_fossil(rec)
        s = 'interpreted %s as fossil' % rec['basisofrecord']
        self.assertFalse(b, s)
        
        rec['networks'] = 'MaNIS,VertNet,Paleo'
        b = is_fossil(rec)
        s = 'did not interpret %s as fossil' % rec['networks']
        self.assertTrue(b, s)
        
        rec['networks'] = 'MaNIS,ORNIS,VertNet'
        b = is_fossil(rec)
        s = 'interpreted %s as fossil' % rec['networks']
        self.assertFalse(b, s)
        
    def test_has_typestatus(self):
        print 'testing has_typestatus'
        rec={}
        b = has_typestatus(rec)
        s = 'interpreted rec as having typestatus when rec is empty'
        self.assertFalse(b, s)

        rec['typestatus'] = ''
        b = has_typestatus(rec)
        s = 'interpreted rec as having typestatus when typestatus is empty'
        self.assertFalse(b, s)

        rec['typestatus'] = 'holotype'
        b = has_typestatus(rec)
        s = 'interpreted rec as not having typestatus: %s' % rec
        self.assertTrue(b, s)

        rec['typestatus'] = 'anything'
        b = has_typestatus(rec)
        s = 'interpreted rec as not having typestatus: %s' % rec
        self.assertTrue(b, s)

    def test_was_captive(self):
        print 'testing was_captive'
        rec={}
        b = was_captive(rec)
        s = 'interpreted rec as having been captive when rec is empty'
        self.assertFalse(b, s)

        rec['establishmentmeans'] = ''
        b = was_captive(rec)
        s = 'interpreted rec as having been captive without evidence'
        self.assertFalse(b, s)

        rec['establishmentmeans'] = 'managed'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec['establishmentmeans'] = 'wild caught'
        b = was_captive(rec)
        s = 'interpreted rec as being captive: %s' % rec
        self.assertFalse(b, s)

        rec['occurrenceremarks'] = 'bread in captivity'
        b = was_captive(rec)
        s = 'interpreted rec as being captive: %s' % rec
        self.assertFalse(b, s)

        rec['establishmentmeans'] = 'CAPTIVE'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['locality'] = 'local aviary'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['highergeography'] = 'NORTH AMERICA|CAPTIVE'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['occurrenceremarks'] = 'born in captivity'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['locationremarks'] = 'lab born'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['eventremarks'] = 'from S.D. Zoo'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['occurrenceremarks'] = 'loaned to Museum of Vertebrate Zoology'
        b = was_captive(rec)
        s = 'interpreted rec as being captive: %s' % rec
        self.assertFalse(b, s)

        rec={}
        rec['fieldnotes'] = 'AVIARY SPECIMEN'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['locationremarks'] = 'used boundaries of Kalamazoo for uncertainty'
        b = was_captive(rec)
        s = 'interpreted rec as being captive: %s' % rec
        self.assertFalse(b, s)

        rec={}
        rec['samplingprotocol'] = 'donated from zoo'
        b = was_captive(rec)
        s = 'interpreted rec as not being captive: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['samplingprotocol'] = 'trap method publish in J. Zool.'
        b = was_captive(rec)
        s = 'interpreted rec as being captive: %s' % rec
        self.assertFalse(b, s)

    def test_has_tissue(self):
        print 'testing has_tissue'
        rec={}
        b = has_tissue(rec)
        s = 'interpreted rec as having tissues when rec is empty'
        self.assertFalse(b, s)

        rec['preparations'] = ''
        b = has_tissue(rec)
        s = 'interpreted rec as having tissues when typestatus is empty'
        self.assertFalse(b, s)

        rec['preparations'] = 'frozen carcass'
        b = has_tissue(rec)
        s = 'interpreted rec as not having tissues: %s' % rec
        self.assertTrue(b, s)

    def test_has_media(self):
        print 'testing has_media'
        rec={}
        b = has_media(rec)
        s = 'interpreted rec as having media when rec is empty'
        self.assertFalse(b, s)

        rec['associatedmedia'] = ''
        b = has_media(rec)
        s = 'interpreted rec as having media when associatedmedia is empty'
        self.assertFalse(b, s)

        rec['associatedmedia'] = 'anything'
        b = has_media(rec)
        s = 'interpreted rec as not having media: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['dctype'] = ''
        b = has_media(rec)
        s = 'incorrectly interpreted rec as having media: %s' % rec
        self.assertFalse(b, s)

        rec['dctype'] = 'anything'
        b = has_media(rec)
        s = 'incorrectly interpreted rec as having media: %s' % rec
        self.assertFalse(b, s)

        rec['dctype'] = 'Sound'
        b = has_media(rec)
        s = 'interpreted rec as not having media: %s' % rec
        self.assertTrue(b, s)

        rec['dctype'] = 'MovingImage'
        b = has_media(rec)
        s = 'interpreted rec as not having media: %s' % rec
        self.assertTrue(b, s)

        rec['dctype'] = 'StillImage'
        b = has_media(rec)
        s = 'interpreted rec as not having media: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['basisofrecord'] = ''
        b = has_media(rec)
        s = 'incorrectly interpreted rec as having media: %s' % rec
        self.assertFalse(b, s)

        rec['basisofrecord'] = 'PreservedSpecimen'
        b = has_media(rec)
        s = 'incorrectly interpreted rec as having media: %s' % rec
        self.assertFalse(b, s)

        rec['basisofrecord'] = 'HumanObservation'
        b = has_media(rec)
        s = 'incorrectly interpreted rec as having media: %s' % rec
        self.assertFalse(b, s)

        rec['basisofrecord'] = 'MachineObservation'
        b = has_media(rec)
        s = 'interpreted rec as not having media: %s' % rec
        self.assertTrue(b, s)

    def test_vn_type(self):
        print 'testing vn_type'
        rec={}
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'indeterminate', s)

        rec['basisofrecord'] = ''
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'indeterminate', s)

        rec['basisofrecord'] = 'voucher'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'specimen', s)

        rec['basisofrecord'] = 'PreservedSpecimen'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'specimen', s)

        rec['basisofrecord'] = 'HumanObservation'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'observation', s)

        rec['basisofrecord'] = 'MachineObservation'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'observation', s)

        rec={}
        rec['dctype'] = 'PhysicalObject'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'specimen', s)

        rec['dctype'] = 'Sound'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'observation', s)

        rec['dctype'] = 'StillImage'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'observation', s)

        rec['dctype'] = 'MovingImage'
        b = vn_type(rec)
        s = 'incorrect vn_type characterization - %s. rec: %s' % (b, rec)
        self.assertEqual(b, 'observation', s)

    def test_has_binomial(self):
        print 'testing has_binomial'
        rec={}
        b = has_binomial(rec)
        s = 'interpreted rec as having binomial when rec is empty'
        self.assertFalse(b, s)

        rec['genus'] = ''
        b = has_binomial(rec)
        s = 'interpreted rec as having binomial when genus is empty'
        self.assertFalse(b, s)

        rec['genus'] = 'Ctenomys'
        b = has_binomial(rec)
        s = 'incorrectly interpreted rec as having binomial: %s' % rec
        self.assertFalse(b, s)

        rec['specificepithet'] = 'socabilis'
        b = has_binomial(rec)
        s = 'incorrectly interpreted rec as not having binomial: %s' % rec
        self.assertTrue(b, s)

        rec={}
        rec['specificepithet'] = 'socabilis'
        b = has_binomial(rec)
        s = 'interpreted rec as having binomial when genus is empty'
        self.assertFalse(b, s)

        rec={}
        rec['scientificname'] = ''
        b = has_binomial(rec)
        s = 'interpreted rec as having binomial when genus is empty'
        self.assertFalse(b, s)

        rec['scientificname'] = 'Ctenomys'
        b = has_binomial(rec)
        s = 'interpreted rec as having binomial when genus is empty'
        self.assertFalse(b, s)

        rec['scientificname'] = 'Ctenomys sociabilis'
        b = has_binomial(rec)
        s = 'incorrectly interpreted rec as not having binomial: %s' % rec
        self.assertTrue(b, s)

        rec['scientificname'] = 'Panthera tigris tigris'
        b = has_binomial(rec)
        s = 'incorrectly interpreted rec as not having binomial: %s' % rec
        self.assertTrue(b, s)

    def test_rank(self):
        print 'testing rank'
        rec={}
        b = rec_rank(rec)
        expected = 0
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['genus'] = 'Something'
        b = rec_rank(rec)
        expected = 0
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['specificepithet'] = 'else'
        b = rec_rank(rec)
        expected = 1
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['year'] = ''
        b = rec_rank(rec)
        expected = 1
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['year'] = '-1'
        b = rec_rank(rec)
        expected = 1
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['year'] = '1'
        b = rec_rank(rec)
        expected = 2
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['month'] = ''
        b = rec_rank(rec)
        expected = 2
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['month'] = '14'
        b = rec_rank(rec)
        expected = 2
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['month'] = 'x'
        b = rec_rank(rec)
        expected = 2
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['month'] = '3'
        b = rec_rank(rec)
        expected = 3
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['day'] = ''
        b = rec_rank(rec)
        expected = 3
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['day'] = 0
        b = rec_rank(rec)
        expected = 3
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['day'] = '33'
        b = rec_rank(rec)
        expected = 3
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['day'] = '17'
        b = rec_rank(rec)
        expected = 4
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['decimallatitude'] = '1'
        b = rec_rank(rec)
        expected = 4
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['decimallongitude'] = '1'
        b = rec_rank(rec)
        expected = 8
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec.pop('day')
        b = rec_rank(rec)
        expected = 7
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec.pop('month')
        b = rec_rank(rec)
        expected = 6
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec.pop('year')
        b = rec_rank(rec)
        expected = 5
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['geodeticdatum'] = 'WGS84'
        b = rec_rank(rec)
        expected = 5
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['coordinateuncertaintyinmeters'] = '10'
        b = rec_rank(rec)
        expected = 9
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['year'] = '2016'
        b = rec_rank(rec)
        expected = 10
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['month'] = '2'
        b = rec_rank(rec)
        expected = 11
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

        rec['day'] = '9'
        b = rec_rank(rec)
        expected = 12
        s = 'rank %s not as expected: %s' % (b, expected)
        self.assertEqual(b, expected, s)

if __name__ == '__main__':
    print '=== vn_utils.py ==='
    unittest.main()
