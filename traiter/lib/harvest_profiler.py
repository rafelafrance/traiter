import cProfile
import re
from harvest_record_processor import VertHarvestFileProcessor

def main():
    inputfile = './tests/data/cuml_sound_film/input_cuml_sound_film_aa'
    outputfile = './tests/data/cuml_sound_film/output_cuml_sound_film_aa'
    includeheader = 'noheader'

    processor = VertHarvestFileProcessor()
    processor.parse_harvest_file(inputfile, outputfile, includeheader)

if __name__ == '__main__':
    main()
