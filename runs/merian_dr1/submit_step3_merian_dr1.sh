# \\ User inputs
SCRIPTNAME="$1"
echo Running $SCRIPTNAME with Merian DR1 Step 3 settings

# \\ Load the right version of LSSTPipe
LSST_CONDA_ENV_NAME=lsst-scipipe-4.0.1 
source "/projects/HSC/LSST/stack/loadLSST.sh"
setup lsst_distrib -t w_2022_29
eups list lsst_distrib | grep setup

# \\ set up the ctrl_bps_parsl repo
cd ctrl_bps_parsl/
setup -j -r .

# \\ set up necessary variables to orient BPS
REPO=/projects/MERIAN/repo
GPFSDIR=/scratch/gpfs/$USER
LOGDIR=$GPFSDIR/logs


cd $GPFSDIR; \
LOGFILE=$LOGDIR/merian_dr1_step3_BPS_"$SCRIPTNAME"_$(date +%F).log; \
BPSYAML=/tigress/kadofong/merian/data_reduction/scripts/merian_dr1/bps/merian_dr1_step3_"$SCRIPTNAME".yaml
echo "Started by $USER on $(date +%F)" > "$BPSYAML".lock
export OMP_NUM_THREADS=1; \
export NUMEXPR_MAX_THREADS=1; \
date | tee -a $LOGFILE; \
$(which time) -f "Total runtime: %E" \
bps submit $BPSYAML \
2>&1 | tee -a $LOGFILE; \
date | tee -a $LOGFILE

