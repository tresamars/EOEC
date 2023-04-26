#source /Users/theresamarschall/Documents/envs/envInzicht/bin/activate
#sys.argv[1]  can be used to give input to script e.g. filter_inzicht.py hello results in sys.argv[1] being hello
import os
import sys
#import matplotlib.pyplot as plt #to enable plotting within notebook
from nilearn import image as nimg
from nilearn import plotting as nplot
from bids.layout import BIDSLayout
import numpy as np
import nibabel as nib
import pandas as pd


fmriprep_dir = '/data/p272412/Inzicht_Button' #'/Volumes/Seagate/Inzicht/fmriprep/'
layout=BIDSLayout(fmriprep_dir, validate=False,
                  config=['bids','derivatives'])
high_pass= 0.01
low_pass = None
t_r = 2
confound_vars = ['csf', 'white_matter']

sub = sys.argv[1] 
sub = sub[-4:]

print(sub)
T1w_files = layout.get(subject=sub,
                    datatype='anat', desc='preproc',
                    space='MNI152NLin2009cAsym',
                    extension="nii.gz",
                    return_type='file')

brainmask_files = layout.get(subject=sub,
                            datatype='anat', suffix='mask',
                            desc='brain',
                            space='MNI152NLin2009cAsym',
                            extension="nii.gz",
                        return_type='file')

func_files = layout.get(subject=sub, desc='smoothAROMAnonaggr',
                    datatype='func', 
                    extension="nii.gz",
                    return_type='file')

func_mask_files = layout.get(subject=sub,
                            datatype='func', suffix='mask',
                            desc='brain',
                            space='MNI152NLin2009cAsym',
                            extension="nii.gz",
                            res='2',
                        return_type='file')

confound_files = layout.get(subject=sub,
                        datatype='func', 
                        desc='confounds',
                        extension="tsv",
                        return_type='file')

print(func_files,func_mask_files,confound_files,brainmask_files)
func_file = func_files[0]
func_mask_file = func_mask_files[0]
confound_file = confound_files[0]
anat_mask = brainmask_files[0]

confound_df = pd.read_csv(confound_file, delimiter='\t')
final_confounds = confound_vars #+ derivative_columns
confound_df = confound_df[final_confounds]

raw_func_img = nimg.load_img(func_file)
func_mask=nimg.load_img(func_mask_file)

if (raw_func_img.shape != func_mask.shape):
    func_mask=nimg.resample_to_img(func_mask,func_file,interpolation='nearest')

clean_img = nimg.clean_img(raw_func_img,confounds=confound_df,detrend=False,standardize=False,
                        low_pass=low_pass,high_pass=high_pass,t_r=t_r, mask_img=func_mask)

out_name=(func_file[:-7]+ '_filt.nii.gz')
mask_name=(func_mask_file[:-7]+ '_filt.nii.gz')

clean_img.to_filename(out_name)
func_mask.to_filename(mask_name)













