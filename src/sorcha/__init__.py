from . import modules
from . import readers
from . import lightcurves
from .sorcha import cite

# Attempt to import sorcha_community_utils [SCU]. Sorcha does not depend on SCU
# and will not include it during a typical installation. If plugins from SCU are
# desired, the user should install SCU manually in their virtual environment
# prior to executing Sorcha.
try:
    from sorcha_addons import *
except ModuleNotFoundError:
    pass

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")
