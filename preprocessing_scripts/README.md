# Preprocessing

This folder contains all the scripts and files that were used to preprocess the data to the format that is now 
available in this repo. The scripts do not have to be run again as they will only reproduce the data. 

## Preprocessing Pipeline
The data for this corpus has been preprocessed in the following steps:

1. <mark>not published</mark>: ``.edf`` files
: files written by the eye-tracker, non-human readable

2. <mark>not published</mark>: ``.asc`` files
: .edf files converted to human-readable files, includes eye-tracker messages etc. 

3. <mark>published</mark>: ``.tsv`` files
: .asc files parsed into .tsv files, contains one sample per line.

4. <mark>published</mark>: Original fixation report
: Based on the tsv files we used the SR Research Data Viewer to create a fixation report: ``eyetracking_data/original_uncorrected_fixation_report.txt``.

5. <mark>published</mark>: Manually corrected fixation files
: A script was used to manually correct the fixations as they were not always aligned correctly. The script to correct the fixations is _not published_.
The corrected fixations files per reader and text are available in the folder ``eyetracking_data/fixations``.


## Scripts

### `create_word_roi_limits.py`
Used to create the files `word_limits.json` and `sent_limits.json`.
This code creates a list consisting of two lists containing the first and the last roi (i.e., char_index_in_text) of 
a word. These lists  will be used to create the mapping between characters (rois) and words (word_index_in_text) for all
items.

### `char_index_to_word_index.py`
Used to create the file `roi_to_word.tsv`.
This code creates a file containing the mapping of the character-based rois to the word-based word_index_in_text.

## Additional  files
### `word_limits.json` & `sent_limits.json`

These files contain a list for each text. Each list contains another two lists containing the first and last roi of each word / sentence of each text. Example: `b0[0][3]` in `word_limits.json` is the roi (=CURRENT_FIX_INTEREST_AREA_INDEX in the Data Viewer fixation report) where the 4th word of text b0 begins and
`b0[1][3]` is the roi where the 4th words ends (i.e., the position of the last character of this word). These
limits are computed in the script ``create_word_roi_limits.py``

The same is true for the sentence limits, just on sentence level.

### `roi_to_word.tsv`

This file contains a mapping from the roi (char_index_in_text) to the word index in each text (word_index_in_text). 
This file is created by the script ``char_index_to_word_index.py``.
