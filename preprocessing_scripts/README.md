# Preprocessing

This folder contains all the scripts and files that were used to preprocess the data to the format that is now 
available in this repo. The scripts do not have to be run again as they will only reproduce the data. 

## Preprocessing Pipeline
The data for this corpus has been preprocessed in the following steps:

1. <mark>not published</mark>: ``.edf`` files
: files written by the eye-tracker, non-human readable

2. <mark>published</mark>: ``.asc`` files
: .edf files converted to human-readable files, includes eye-tracker messages etc. 

3. <mark>published</mark>: ``.csv`` files
: .asc files parsed into .tsv files, contains one sample per line. Script ``parse_asc_files.py`` creates the ``.csv`` file from the `.asc` files.

4. <mark>published</mark>: Original fixation report
: Based on the csv files we used the SR Research Data Viewer to create a fixation report. ``OSF/eyetracking_data/FixRep_20_Mai_2017.txt``.

5. <mark>unpublished</mark>: Manually corrected fixation report
: We used a script to manually correct the fixations as they were not always aligned correct. The script to correct the fixations is not published either. 


6. <mark>published</mark>: `.txt` fixation files per reader and text
: containing reading measures / fixations per text and reader. Note that the script ``split_fixation_report.py`` 
**cannot** be used to recreate these files exactly as the fixation report has been manually corrected and some columns have been added.

## Scripts

All these scripts can be run from the `preprocessing_scripts` folder without providing any arguments to reproduce the files. 
If they are run from another location, all paths need to be provided as arguments.

### `char_index_to_word_index.py`
Used to create the file `roi_to_word.tsv` (see below).

*Old comment: March 7, 2017
Lena Jaeger
File for data preprocessing_scripts of "ExpertReading"
This code creates a file containing the mapping of the character-based rois to the word-based WordIndexInText*

### `compute_reading_measures.py`
<mark>TODO</mark>

### `create_word_roi_limits.py`
Used to create the files `word_limits.json` and `sent_limits.json` (see below).

*Lenas old comment: March 7, 2017 Lena Jaeger File for data preprocessing_scripts of "ExpertReading" This code creates a list consisting of two
lists containing the first and the last roi (i.e., character index in a text) of a word. These lists (
<itemid>_Limits) will be used to create the mapping between characters (rois) and words (wordIndexInText) for all
items.*

### `parse_asc_files.py`
<mark>TODO</mark>

*Old comment: This script extracts the lines with samples (timestamp, x-screen coordinate, y-screen coordinate, pupil diameter)
from Eyelink 100 raw data files (previously converted from edf to ascii).
The data was recorded with different scripts; in some sesssions, practice trials (e.g. session  1.asc) were recorded,
in most sessions not. In the sessions where practice trials were recorded, all trial variables TRIAL_VAR were written
12 times rather than once to the data (always after the eye mov samples have been written).
This script handles both kinds of data files.*

### `split_fixation_report.py`
Used to split the fixation report created by the Data Viewer into individual fixations files for each text and reader. 
In addition, it creates a file containing all reader IDs (RECORDING_SESSION_LABEL) `participants/readerIDs.txt`.

*Note: as we do not provide the corrected fixation report (see preprocessing pipeline), this script cannot be used 
to recreate the fixation files provided in the repository!*

## Additional  files
### `word_limits.json` & `sent_limits.json`

These files contain a list for each text. Each list contains another two lists containing the first and last roi of each word / sentence of each text. Example: `b0[0][3]` in `word_limits.json` is the roi (=CURRENT_FIX_INTEREST_AREA_INDEX in the Data Viewer fixation report) where the 4th word of text b0 begins and
`b0[1][3]` is the roi where the 4th words ends (i.e., the position of the last character of this word). These
limits are computed in the script ``create_word_roi_limits.py``

The same is true for the sentence limits, just on sentence level.

### `roi_to_word.tsv`

This file contains a mapping from the roi (=char index) to the word index in each text. This file is created by the script ``char_index_to_word_index.py``.
