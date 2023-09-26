import cProfile
import pstats

from pstats import SortKey
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

"""
Run this script from inside the benchmarks directory so that the relative file
path for the database is correct.

Notes:
The results indicate that the vast majority of the time spent in this function
is used to read the data in the sqlite db file. 

I've attempted to optimize the query to avoid renaming columns, and I've tried
removing the `order by`; replacing it with in-memory sorting in pandas. Both
resulted in longer run times for PPReadPointingDatabase.

I've also attempted to optimize the `isin` operation at the end of ReadPointingDb
by creating a combined mask (`or`-ing together the masks for each individual
filter) and then applying that. This also resulting in a longer run time.

Converting the input list, `observing_filters`, to a pandas `Series` seems to
have no affect despite some online rumors that it might help the performance of
`isin`.
https://stackoverflow.com/questions/23945493/a-faster-alternative-to-pandas-isin-function
"""

filter_list = ["u", "g", "r", "i", "z", "y"]

sql_query = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId"

cProfile.run("PPReadPointingDatabase('../demo/baseline_v2.0_1yr.db', filter_list, sql_query)", "restats")

p = pstats.Stats("restats")
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(30)
