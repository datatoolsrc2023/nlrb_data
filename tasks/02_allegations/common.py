import sys
from pathlib import Path

# Get the absolute path of the repo
project_path = Path(__file__).absolute().parent.parent.parent
sys.path.insert(0, str(project_path))

# We uppercase the Common/ package to avoid a conflict here
# If we lower-cased, then the common.py module (common) would instead try to import itself.
from Common import *
