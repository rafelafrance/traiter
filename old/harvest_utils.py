from vn_utils import read_header
import csv

def get_harvest_folders_from_file(inputfile):
    '''
       Create a list of folders on Google Cloud Storage to process. List comes from
       inputfile, which must contain the fields:
           icode, gbifdatasetid, harvestfoldernew
    '''
    harvestfolders = []
    fieldnames = ['icode', 'gbifdatasetid', 'harvestfolder']

    dialect = csv.excel

    header = read_header(inputfile, dialect)
#    print 'header: %s' % header
    if header is None:
        print 'Can not read header from %s.' % inputfile
        return None

    # Populate the list of folders to harvest from the inputfile
    with open(inputfile, 'r') as infile:
        reader = csv.DictReader(infile, dialect=dialect, fieldnames=header)
        reader.next()
        for field in fieldnames:
           if field not in header:
               print 'Required field %s not found in %s.' % (field, inputfile)
               return None
        for row in reader:
            newrow = {}
#            print 'row: %s' % row
            for field in fieldnames:
                newrow[field]=row[field]
            harvestfolders.append(row)
    return harvestfolders
