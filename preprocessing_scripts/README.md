# Preprocessing

This folder contains all the scripts and files that were used to preprocess the data to the format that is now 
available in this repo. The scripts do not have to be run again as they will only reproduce the data. 

## word_limits.json & sent_limits.json

The lists below contain the first and last roi of each word of a text. E.g., `b0[0][3]` is the roi (
=CURRENT_FIX_INTEREST_AREA_INDEX in the Data Viewer fixation report) where the 4th word of text b0 begins and
`b0[1][3]` is the roi where the 4th words ends (i.e., the position of the last character of this word). These
limits are computed in the script ``create_word_roi_limits.py``

The same is true for the sentence limits, just on sentence level.

## Preprocessing Pipeline
The data for this corpus has been preprocessed in the following steps:

1. <mark>not published</mark>: .edf files
: files written by the eye-tracker, non-human readable

2. <mark>published</mark>: .asc files
: .edf files converted to human-readable files, includes eye-tracker messages etc. 

3. <mark>published</mark>: .csv files
: .asc files parsed into .csv files, contains one sample per line. Script ``parse_asc_files.py`` creates the .csv file from the .asc files.

4. <mark>published</mark>: Fixation report
: Based on the csv files we used the SR Research Data Viewer to create a fixation report. ``OSF/eyetracking_data/FixRep_20_Mai_2017.txt``.


5. <mark>unpublished</mark>: Manually corrected fixation report
: We used a script to manually correct the fixations as they were not always aligned correct. 


6. <mark>published</mark>: .txt fixation files per reader and text
: containing reading measures / fixations per text and reader. Note that the script ``split_fixation_report.py`` 
**cannot** be used to recreate these files exactly as the fixation report has been manually corrected and some columns have been added.