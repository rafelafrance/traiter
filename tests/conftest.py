"""Setup the test environment."""

import sys
from os.path import dirname, abspath, join


ROOT_DIR = join(dirname(dirname(abspath(__file__))), 'traiter')
print(ROOT_DIR)
sys.path.append(ROOT_DIR)
