import re
import sys
import csv
from datetime import datetime
from trait_parsers.body_mass_parser import BodyMassParser
from trait_parsers.life_stage_parser import LifeStageParser
from trait_parsers.sex_parser import SexParser
from trait_parsers.total_length_parser import TotalLengthParser

# need to install regex for this to be used
# pip install regex

# Fields expected in the input from the VertNet harvester:
#    https://github.com/VertNet/gulo
HARVEST_FIELDS = ['icode', 'title', 'citation', 'contact', 'dwca', 'email', 'eml', 
    'emlrights', 'gbifdatasetid', 'gbifpublisherid', 'doi', 'iptlicense', 'migrator', 
    'networks', 'orgcountry', 'orgname', 'orgstateprovince', 'pubdate', 'source_url', 
    'url', 'id', 'associatedmedia', 'associatedoccurrences', 'associatedorganisms', 
    'associatedreferences', 'associatedsequences', 'associatedtaxa', 'bed', 'behavior', 
    'catalognumber', 'continent', 'coordinateprecision', 'coordinateuncertaintyinmeters', 
    'country', 'countrycode', 'county', 'dateidentified', 'day', 'decimallatitude', 
    'decimallongitude', 'disposition', 'earliestageorloweststage', 
    'earliesteonorlowesteonothem', 'earliestepochorlowestseries', 
    'earliesteraorlowesterathem', 'earliestperiodorlowestsystem', 'enddayofyear', 
    'establishmentmeans', 'eventdate', 'eventid', 'eventremarks', 'eventtime', 
    'fieldnotes', 'fieldnumber', 'footprintspatialfit', 'footprintsrs', 'footprintwkt', 
    'formation', 'geodeticdatum', 'geologicalcontextid', 'georeferencedby', 
    'georeferenceddate', 'georeferenceprotocol', 'georeferenceremarks', 
    'georeferencesources', 'georeferenceverificationstatus', 'group', 'habitat', 
    'highergeography', 'highergeographyid', 'highestbiostratigraphiczone', 
    'identificationid', 'identificationqualifier', 'identificationreferences', 
    'identificationremarks', 'identificationverificationstatus', 'identifiedby', 
    'individualcount', 'island', 'islandgroup', 'latestageorhigheststage', 
    'latesteonorhighesteonothem', 'latestepochorhighestseries', 
    'latesteraorhighesterathem', 'latestperiodorhighestsystem', 'lifestage', 
    'lithostratigraphicterms', 'locality', 'locationaccordingto', 'locationid', 
    'locationremarks', 'lowestbiostratigraphiczone', 'materialsampleid', 
    'maximumdepthinmeters', 'maximumdistanceabovesurfaceinmeters', 
    'maximumelevationinmeters', 'member', 'minimumdepthinmeters', 
    'minimumdistanceabovesurfaceinmeters', 'minimumelevationinmeters', 'month', 
    'municipality', 'occurrenceid', 'occurrenceremarks', 'occurrencestatus', 
    'organismid', 'organismname', 'organismremarks', 'organismscope', 
    'othercatalognumbers', 'pointradiusspatialfit', 'preparations', 
    'previousidentifications', 'recordedby', 'recordnumber', 'reproductivecondition', 
    'samplingeffort', 'samplingprotocol', 'sex', 'startdayofyear', 'stateprovince', 
    'typestatus', 'verbatimcoordinates', 'verbatimcoordinatesystem', 'verbatimdepth', 
    'verbatimelevation', 'verbatimeventdate', 'verbatimlatitude', 'verbatimlocality', 
    'verbatimlongitude', 'verbatimsrs', 'waterbody', 'year', 'dctype', 'modified', 
    'language', 'license', 'rightsholder', 'accessrights', 'bibliographiccitation', 
    'references', 'institutionid', 'collectionid', 'datasetid', 'institutioncode', 
    'collectioncode', 'datasetname', 'ownerinstitutioncode', 'basisofrecord', 
    'informationwithheld', 'datageneralizations', 'dynamicproperties', 'taxonid', 
    'scientificnameid', 'acceptednameusageid', 'parentnameusageid', 
    'originalnameusageid', 'nameaccordingtoid', 'namepublishedinid', 'taxonconceptid', 
    'scientificname', 'acceptednameusage', 'parentnameusage', 'originalnameusage', 
    'nameaccordingto', 'namepublishedin', 'namepublishedinyear', 'higherclassification', 
    'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'subgenus', 
    'specificepithet', 'infraspecificepithet', 'taxonrank', 'verbatimtaxonrank', 
    'scientificnameauthorship', 'vernacularname', 'nomenclaturalcode', 'taxonomicstatus', 
    'nomenclaturalstatus', 'taxonremarks']

# Trait fields to add to the header for the output
TRAIT_FIELDS = ['haslength', 'haslifestage', 'hasmass', 'hassex', 'lengthinmm', 'massing',
    'lengthunitsinferred', 'massunitsinferred', 'derivedlifestage', 'derivedsex']

# Fields added for indexing
INDEX_FIELDS = ['keyname', 'rank', 'haslicense', 'vntype']

# Fields to go in the output
OUTPUT_FIELDS = HARVEST_FIELDS + INDEX_FIELDS + TRAIT_FIELDS

class VertHarvestFileProcessor:

    def __init__(self):
        self.body_mass_parser    = BodyMassParser()
        self.life_stage_parser   = LifeStageParser()
        self.sex_parser          = SexParser()
        self.total_length_parser = TotalLengthParser()

    def parse_row(self, row):
        strings = [row['dynamicproperties'], row['occurrenceremarks'], row['fieldnotes']]
        traits  = self.sex_parser.preferred_or_search(row['sex'], strings)
        traits.update(self.life_stage_parser.preferred_or_search(row['lifestage'], strings))
        traits.update(self.total_length_parser.search_and_normalize(strings))
        traits.update(self.body_mass_parser.search_and_normalize(strings))
        return traits

    def parse_harvest_file(self, infilename, outfilename, header=None):
        # fields from the original harvest files
        dialect = tsv_dialect()

        # A header is not used in VertNet indexing chunks. The field order must be defined
        # in the indexer. A header can be added to the output file by setting the optional
        # header parameter
        if header is not None:
            with open(outfilename, 'w') as outfile:
                writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=OUTPUT_FIELDS)
                writer.writeheader()

        with open(outfilename, 'a') as outfile:
            writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=OUTPUT_FIELDS)

            with open(infilename, 'r') as infile:
                reader = csv.DictReader(infile, dialect=dialect, fieldnames=HARVEST_FIELDS)
                for row in reader:
#                    print 'row: %s' % row
                    newrow = self.process_harvest_row(row)
#                    print 'newrow: %s' % newrow
                    wrong_fields = [k for k in newrow if k not in OUTPUT_FIELDS]
#                    print 'wrong fields: %s' % wrong_fields
                    writer.writerow(newrow)

    def process_harvest_row(self, row):
        """Produces an output record ready for indexing based on a post-harvest input 
           record with structure determined by HARVEST_FIELDS. Adds new fields and 
           changes contents of some existing fields."""
        
        ### RECORD IDENTIFIER ###
        # Create a record identifier - docid in Google App Engine documents
        # Create a slugged version of the resource title (from the Darwin Core archive's
        # metadata) as a resource identifier
        # Harvest row is assumed to have 'title' field
        resource_slug = slugify(row['title'])

        # Create a condensed version of the icode (Institution Code from VertNet registry)
        # as an institution identifier
        # Harvest row is assumed to have 'icode' field
        icode_slug = re.sub(" ","", row['icode'].lower())
    
        # Create a condensed version of the collectioncode as a collection identifier
        # Harvest row is assumed to have 'collectioncode' field
        coll_id = ''
        # If the collectioncode has content, use it for the collection identifier
        # otherwise, use the slugged version of the resource identifier
        if row['collectioncode'] is not None and len(row['collectioncode']) > 0:
            coll_id = re.sub(' ','-', re.sub("\'",'',repr(row['collectioncode'])).lower())
        else:
            coll_id = re.sub("\'",'',repr(resource_slug))
    
        # Create a condensed version of the occurrence identifier
        # Harvest row is assumed to have 'catalognumber' field and an occurrenceid field
        # If the catalognumber has content, use if for the occurrence identifier
        # otherwise, use the ocurrenceid if it has content
        # otherwise, use 'noid'
        occ_id = ''
        if row['catalognumber'] is not None and len(row['catalognumber']) > 0:        
            occ_id = re.sub("\'",'',repr(slugify(row['catalognumber'])))
        else:
            if row['id'] is not None and len(row['id']) > 0:
                occ_id = 'oid-%s' % re.sub("\'",'',repr(row['id']))
            else:
                occ_id = 'noid'

        # Make a "potentially persistent" resource identifier
        # Note that this is dependent on the persistence of the resource 'title' and 
        # the VertNet registry 'icode' If these change, the record ids will change and the
        # resource will have to be purged from the data store before re-indexing
        res_id = '%s/%s' % (icode_slug, resource_slug)

        # Make a unique, potentially persistent record (datastore document) identifier
        keyname = '%s/%s/%s' % (icode_slug, coll_id, occ_id)
        # The keyname is the record identifier. Add it to the output data
        row['keyname'] = keyname

        ### EVENTDATE ###
        # Make an eventdate from year, month, day if there is no eventdate
        eventdate = _eventdate(row)

        ### YEAR, MONTH, DAY ###
        # Make year, month, day from eventdate if the three are not all populated
        year, month, day = _ymd_from_event_date(eventdate)

        ### GEOREFERENCE ###
        unc = _coordinateuncertaintyinmeters(row['coordinateuncertaintyinmeters'])
        print 'cordunc: %s unc: %s' % (row['coordinateuncertaintyinmeters'], unc)

        ### REFERENCES ###
        # VertNet migrator must construct the references field using this same pattern for 
        # records that do not already have a references value.
        if row['references'] is None or len(row['references'])==0:
            references = 'http://portal.vertnet.org/o/%s/%s?id=%s' % \
              (icode_slug, coll_id, occ_id)
            row['references']=references

        ### LICENSES ###
        # Translate the field 'iptlicense' to field 'license' if the latter is missing
        # Harvest row is assumed to have 'license' and 'iptlicense' fields
        if row['license'] is None:
            row['license']=row['iptlicense']
        if row['license'] is None and row['iptlicense'] is None:
            row['haslicense']=0
        else:
            row['haslicense']=1
        
        ### TRAITS ###
        # Add the process the traits and add trait fields to the record 
        traits = self.parse_row(row)
        print 'traits:\n%s' % traits
        for trait in traits:
            row[trait]=traits[trait]

        ### RANK ###
        # The index has a default sort order. In VertNet we set it based on rank, which 
        # is a rough assessment of fitness for a variety of uses.
        row['rank'] = _rank(row)
        
        # Return the index-ready row        
        return row

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

def _rank(row):
    """Return the rank to be used in document sorting based on the content priority."""
    if has_binomial(row) is False:
        return 0
    # Must have a binomial to have a non-zero rank.
    rank = 0
    hasgeoref = valid_georef(row)
    hascoords = False
    if hasgeoref is True:
        hascoords = True
    else:
        hascoords = valid_coords(row) 
    hasyear = valid_year(row['year'])
    hasmonth = valid_month(row['month'])
    hasday = valid_day(row['day'])
    
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

def has_binomial(row):
    """Return True if row has content in genus and specificepithet, 
       otherwise return False."""
    # For now it is a sufficient condition to have these DwC terms populated.
    # Later may want to test them against a name authority to determine validity.
    # Note that this does not account for a scientificName that has a binomial
    # and the genus is null.
    if row['genus'] is None or len(row['genus'])==0:
        return False
    if row['specificepithet'] is None or len(row['specificepithet'])==0:
        return False
    return True
    
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
 
def valid_coords(row):
    """Return True if decimallatitude and decimallongitude in rec are in valid ranges, 
       otherwise return False."""
    if row['decimallatitude'] is not None and len(row['decimallatitude'])>0:
        if row['decimallongitude'] is not None and len(row['decimallongitude'])>0:
            return valid_latlng(row['decimallatitude'],row['decimallongitude'])
    return False
 
def valid_georef(row):
    """Return True if rec has valid coords, valid coordinateuncertaintyinmeters, and a 
       geodeticdatum, otherwise return False."""
    if row['coordinateuncertaintyinmeters'] is None or \
       len(row['coordinateuncertaintyinmeters'])==0:
        return False
    if row['geodeticdatum'] is None or len(row['geodeticdatum'])==0:
        return False
    if _coordinateuncertaintyinmeters(row['coordinateuncertaintyinmeters']) is None:
        return False
    if row['decimallatitude'] is None or len(row['decimallatitude'])==0:
        return False
    if row['decimallongitude'] is None or len(row['decimallongitude'])==0:
        return False
    return valid_latlng(row['decimallatitude'],row['decimallongitude'])
 
def _coordinateuncertaintyinmeters(unc):
    """Return the value of unc as a rounded up integer if it is a number greater than 
    zero, otherwise return None."""
    uncertaintyinmeters = is_float(unc)
    if uncertaintyinmeters is None:
        return None
    # Check to see if uncertaintyinmeters is less than one. Zero is not a legal 
    # value. Less than one is an error in concept.
    if uncertaintyinmeters < 1:
        return None
    # Return the nearest rounded up meter.
    return int( round(uncertaintyinmeters + 0.5) )

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
 
# def is_int(str):
#     """Return the value of str as an int if possible, otherwise return None."""
#     # Accepts str as string. Returns int(str) or None
#     if str is None:
#         return None
#     try:
#         f = int(str)
#         return f
#     except ValueError:
#         return None
 
def valid_year(year):
    """Return True if the year is since 1700 and before next year, 
       otherwise return False."""
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
    """Naive day range validity test only for ranking purposes, not for validation.
       Return True if the day is between 1 and 31 inclusive, otherwise return False."""
    # Accepts day as string.
    fday = is_float(day)
    if fday is None:
        return False
    if fday < 1:
        return False
    if fday > 31:
        return False
    return True

def _eventdate(row):
    """Return the eventdate as a datetime.date based on a eventdate if it is a datetime, 
    otherwise on year, month, and day converted to ISO8601."""
    isodate = None
    if row.has_key('eventdate'):
        isodate = row['eventdate']
    else:
        y = rec['year']
        m = rec['month']
        d = rec['day']
        isodate = eventdate_from_ymd(y,m,d)
    
    try:
        eventdate = datetime.strptime(isodate, '%Y-%m-%d').date()
    except:
        eventdate = None        
    return eventdate

def eventdate_from_ymd(ymd):
    """Return the eventdate as ISO8601 based on year y, month m, and day d as strings
    in a tuple (y, m, d)."""
    y, m, d = ymd
    if valid_year(y) is False:
        return None
    hasmonth = valid_month(m)
    hasday = valid_day(d)
    eventdate = str(y)
    if hasmonth is True:
        month = is_float(m)
        if month is not None:
            if month > 9:
                eventdate += '-'+str(m)
            else:
                eventdate += '-0'+str(m)
            if hasday is True:
                day = is_float(d)
                if day is not None:
                    if day > 9:
                        eventdate += '-'+str(d)
                    else:
                        eventdate += '-0'+str(d)
    return eventdate

def _ymd_from_event_date(eventdate):
    """Return a tuple of year month and day derived from a well-behaved eventdate as a
    datetime."""
    if eventdate is None:
        return None
    d = eventdate.split('-')
    year = d[0]
    month = None
    day = None
    if len(d)>1:
        month = d[1]
    if len(d)>2:
        day = d[2]
    return (year, month, day)

def _type(row):
    """Return one of 'specimen', 'observation', or 'both' based on content of the type 
    and basisofrecord fields."""
    if row['basisofrecord'] is None:
        if row['dctype'] is None:
            return 'both'
        elif 'obj' in row['dctype'].lower():
            return 'specimen'
        return 'observation
    if 'obs' in row['basisofrecord'].lower():
        return 'observation'
    return 'specimen'

def tsv_dialect():
    """Get a dialect object with TSV properties.
    parameters:
        None
    returns:
        dialect - a csv.dialect object with TSV attributes"""
    dialect = csv.excel_tab
    dialect.lineterminator='\n'
    dialect.delimiter='\t'
    dialect.escapechar='/'
    dialect.doublequote=True
    dialect.quotechar='"'
    dialect.quoting=csv.QUOTE_NONE
    dialect.skipinitialspace=True
    dialect.strict=False
    return dialect

# Example command line invocation:
# python harvest_record_processor.py testdata-aa-1record outfile.txt yes
# testdata-aa is from data-2015-10-28-uam_herp-753047f9-b2d1-4356-96c8-c84618183efc-aa
if __name__ == "__main__":
    processor = VertHarvestFileProcessor()
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    includeheader = sys.argv[3]
    processor.parse_harvest_file(inputfile, outputfile, includeheader)

# From indexer.py
#        input_class = (input_readers.__name__ + "." +
#                    input_readers.GoogleCloudStorageLineInputReader.__name__)
