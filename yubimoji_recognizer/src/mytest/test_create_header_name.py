import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "./.."
sys.path.append(ROOTPATH)

from output_csv_file import create_header_name


print(create_header_name())