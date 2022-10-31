
import re

template = '''export NUMEXPR_MAX_THREADS=1
export OMP_NUM_THREADS=1

source /projects/HSC/LSST/stack/loadLSST.bash
setup lsst_distrib -t w_2022_12

# \\\\ PROJECT-specific variables
REPO=/projects/MERIAN/repo

# \\\\ USER-specific variables
LOGDIR=/home/kadofong/merian/merian_logs/coadds

# \\\\ RUN-specific variables
TRACT="<TRACTID>"
VISITS="<VISITS>"
RUNNAME=t"$TRACT"_<SUFFIX>

# \\\\ butler work starts here
CHILDREN="DECam/runs/merian/w_2022_02/202103,\\
DECam/runs/merian/w_2022_02/202111,\\
DECam/runs/merian/w_2022_02/202201"

butler collection-chain $REPO DECam/runs/merian/w_2022_02 $CHILDREN # XXX do we need this in this script?

LOGFILE=$LOGDIR/step3_"$RUNNAME"_joint.log
echo "Log is $LOGFILE"
echo "~~~ Let's begin ~~~ "

date | tee $LOGFILE; \\
pipetask --long-log run --register-dataset-types -j 12 \\
-b $REPO --instrument lsst.obs.decam.DarkEnergyCamera \\
-i DECam/runs/merian/w_2022_02 \\
-o DECam/runs/merian/w_2022_02/$RUNNAME \\
-p $OBS_DECAM_DIR/pipelines/DRP.yaml#step3 \\
-d "instrument='DECam' AND skymap='hsc_rings_v1' AND tract=$TRACT AND visit IN $VISITS" \\
2>&1 | tee -a $LOGFILE; \\
date | tee -a $LOGFILE
''' # XXX need to make these parts more moveable

def generate_script ( tractid, visits, suffix='TEST' ):
    if isinstance(visits, str):
        parsed_visits = visits
    elif hasattr(visits, '__getitem__'):
        if hasattr ( visits, 'astype'):
            parsed_visits = '('+','.join(visits.astype(str))+')' # \\ for numpy arrays & pandas
        else:
            parsed_visits = '('+','.join([ str(x) for x in visits ])+')' # \\ for lists
    
    script = template.replace ( '<TRACTID>', str(tractid) ).replace('<VISITS>', parsed_visits).replace('<SUFFIX>', suffix)
    return script
    

