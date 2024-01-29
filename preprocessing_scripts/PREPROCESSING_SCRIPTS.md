# Preprocessing

This folder contains all the scripts and files that were used to preprocess the data to the format that is now 
available in this repo. The scripts do not have to be run again as they will only reproduce the data. 

## Preprocessing Pipeline
The data for this corpus has been preprocessed in the following steps:

1. not published: ``.edf`` files
: files written by the eye-tracker, non-human readable

2. not published: ``.asc`` files
: .edf files converted to human-readable files, includes eye-tracker messages etc. 

3. published: ``.tsv`` files
: .asc files parsed into .tsv files, contains one sample per line.

4. published: Original fixation report
: Based on the tsv files we used the SR Research Data Viewer to create a fixation report: ``eyetracking_data/original_uncorrected_fixation_report.txt``.

5. published: Manually corrected fixation files
: A script was used to manually correct the fixations as they were not always aligned correctly. The script to correct the fixations is _not published_.
The corrected fixations files per reader and text are available in the folder ``eyetracking_data/fixations``.

6. published: Additional preprocessing
: The computed fixations were further processed to obtain the data in different format. Please refer to the folder 
`additional_scripts` adn the respective [README](../additional_scripts/ADDITIONAL_SCRIPTS.md).


## Scripts

### `create_word_aoi_limits.py`
Used to create the files `word_limits.json` and `sent_limits.json`.
This code creates a list consisting of two lists containing the first and the last aoi (i.e., char_index_in_text) of 
a word. These lists  will be used to create the mapping between characters (aois) and words (word_index_in_text) for all
items.

### `char_index_to_word_index.py`
Used to create the file `aoi_to_word.tsv`.
This code creates a file containing the mapping of the character-based aois to the word-based word_index_in_text.

### `asc_to_tsv.py`
This script was used to parse the .asc files into .tsv files.

### `split_fixation_report.py`
This script splits the original fixation report into one file per text and reader. The files are stored in the folder
`eyetracking_data/fixations_uncorrected`.

### `correct_fixations.py`
This is the script that has been used to manually correct the fixations. It allows to go through all fixation files and
visualizes them. For each fixation the user can decide whether it is correct or not. If not, the user can correct the fixation
and move it up or down and update the respective area of interest.


## Additional  files
### `word_limits.json` & `sent_limits.json`

These files contain a list for each text. Each list contains another two lists containing the first and last aoi of each word / sentence of each text. Example: `b0[0][3]` in `word_limits.json` is the aoi (=CURRENT_FIX_INTEREST_AREA_INDEX in the Data Viewer fixation report) where the 4th word of text b0 begins and
`b0[1][3]` is the aoi where the 4th words ends (i.e., the position of the last character of this word). These
limits are computed in the script ``create_word_aoi_limits.py``

The same is true for the sentence limits, just on sentence level.

### `aoi_to_word.tsv`

This file contains a mapping from the aoi (char_index_in_text) to the word index in each text (word_index_in_text). 
This file is created by the script ``char_index_to_word_index.py``.
