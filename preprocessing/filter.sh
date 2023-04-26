#!/bin/bash
#
#SBATCH --time=00:15:00
#SBATCH --partition=short
#SBATCH --mem-per-cpu=5G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --job-name=array-filter-%a
#SBATCH --output=/data/p272412/Inzicht_Button/scripts/out/filter-%a-out.txt
#SBATCH --array=0-6
 
module purge
module load Python/3.10.4-GCCcore-11.3.0 
BIDS_DIR=/data/p272412/Inzicht_Button/bidsdata
#python3 -m venv /data/$USER/envs/Inzicht_Button
#pip install -r requirements.txt
SUBJ=$(awk "NR==$(($SLURM_ARRAY_TASK_ID+2)){print;exit}" $BIDS_DIR/subj.txt | cut -f 1)

echo $SUBJ

source /data/$USER/envs/Inzicht_Button/bin/activate

python3 /data/p272412/Inzicht_Button/scripts/filter.py $SUBJ


 
deactivate