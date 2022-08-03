"""Macros for h5py... because I'm lazy"""

# ! Inside try-except so setup can still grab the __version__ prior to install
try:
    from . import config
    from . import utils
    from . import inspect
    from . import alter
    from . import create
except Exception as e:
    print(e)

__version__ = '0.3.0'