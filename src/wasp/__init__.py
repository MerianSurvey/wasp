import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version(__package__ or __name__)
except:
    __version__ = "dev"

# \\ Check to see if LSST stack is loaded
try:
    import lsst.log
    LSST_INSTALLED = True
except ImportError:
    import warnings
    LSST_INSTALLED = False
    warnings.warn('LSST stack not installed')