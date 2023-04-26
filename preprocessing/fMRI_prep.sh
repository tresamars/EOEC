#!/bin/bash
#
#SBATCH --job-name=array-fmriprep-%a
#SBATCH --output=/data/p272412/EOEC/scripts/out/EOEC-%a-fmriprep-out.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=regular
#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=5G
#SBATCH --mail-type=FAIL
#SBATCH --array=0

# set the name of the participant

FMRIPREP=/data/p272412/singularity/fmriprep.simg
SURF_LICENSE=/data/p272412/freesurfer/license.txt

BIDS_DIR=/data/p272412/EOEC/bids
OUTPUT_DIR=/data/p272412/EOEC/bids/derivatives
WORK_DIR=/scratch/p272412/workdir/EOEC_temp/

SUBJ=$(awk "NR==$(($SLURM_ARRAY_TASK_ID+2)){print;exit}" $BIDS_DIR/sub.txt | cut -f 1)

echo $SUBJ
# run fmriprep

singularity run \
    --bind /data/$USER/EOEC \
    --bind /scratch/$USER/workdir \
    --bind /data/$USER/freesurfer \
    --bind /data/$USER/singularity \
    --cleanenv $FMRIPREP \
    $BIDS_DIR $OUTPUT_DIR participant \
    --n_cpus 4        \
    --omp-nthreads 4 \
    --fs-license-file=$SURF_LICENSE         \
    --participant-label=$SUBJ \
    --skip_bids_validation \
    --output-spaces T1w MNI152NLin2009cAsym:res-2 func MNI152Lin:res-2\
    --use-aroma \
    -w $WORK_DIR