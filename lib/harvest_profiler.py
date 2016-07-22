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

__author__ = "John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "harvest_profiler.py 2016-07-13T09:59+02:00"

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
