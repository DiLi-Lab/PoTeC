# PoTeC Eye-tracking Data

The eye-tracking data is provided in different formats which are explained in this README. The folders are named
accordingly.
One file always contains the data for one reader and one text and is named: "reader[reader_id]_[text_id]_[data_suffix]
.txt".
"data_suffix" refers to the data format and will be explained below for each format.

## fixations

Each file contains the fixations for each word in each text. The data suffix for these files is "fixations".
There files are obtained by splitting the fixation report (`OSF/eyetracking_data/FixRep_20_Mai_2017.txt`) produced 
by the Data  using this script: `OSF/preprocessing/split_fixation_report.py`. NOTE: the fixations were 
manually corrected using this script ``OSF/preprocessing/trim_fixations.py``. The script adds new columns that are now 
in the fixations files in this folder ("line", "index_inline", "ORIGINAL_CURRENT_FIX_INDEX", "Fix_adjusted"). 
If the fixation report is split again using the splitting script these columns 
will be missing!

## reading_measures

Each file in this folder contains the reading measures for each word in each text. The data suffix for these files is "
rm".
The columns are:

## word_order

This folder contains the eye-tracking data for each reader and each text **sequentially ordered by word order in the
text**.
It merges the information in the readingMeasures folder with text and word features and information about the reader and
the experiment.

The data suffix for these files is "merged".
Each file contains the following information:

* all reading measures for each word
* all text features

<ins>Recreate files</ins>

## scanpaths

This folder contains the eye-tracking data for each reader and each text **temporally ordered by fixation**.
The following information is already contained (plus some more):

* information on fixations and saccades
* question accuracies
* word and character indices + actual words and characters

<ins>Recreate files</ins>

The scanpaths can easily be recreated using this script: ``scripts/merge_fixations_word_char.py``.
If the repo is downloaded as-is and the script is run where it is, no paths need to be provided. Otherwise, all paths
can be
provided as arguments. Please see the script for more information.

**NOTE**: the files can be easily merged with the reader information using this script 

