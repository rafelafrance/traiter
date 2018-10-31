import sys
from os.path import dirname, abspath, join


root_dir = join(dirname(dirname(abspath(__file__))), 'traiter')
print(root_dir)
sys.path.append(root_dir)
