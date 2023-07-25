# PoTeC Eye-tracking Data

The eye-tracking data is provided in different formats which are explained in this README. The folders are named
accordingly.
One file always contains the data for one reader and one text and is named according to this scheme:
`reader[reader_id]_[text_id]_[data_suffix].txt`.
"data_suffix" refers to the specific data format.

## fixations

Each file contains the fixations for each word in each text.
There files are obtained by splitting the fixation report (`OSF/eyetracking_data/FixRep_20_Mai_2017.txt`) produced 
by the Data  using this script: `OSF/preprocessing/split_fixation_report.py`. NOTE: the fixations were 
manually corrected using an unpublished script. The script adds new columns that are now 
in the fixations files in this folder ("line", "index_inline", "ORIGINAL_CURRENT_FIX_INDEX", "Fix_adjusted"). 
If the fixation report is split again using the splitting script these columns 
will be missing!

## raw_data
The raw data in readable ``.asc`` format

## reading_measures

Each file in this folder contains the reading measures for each word in each text. The data suffix for these files is "
rm". All the reading measure and their definitions are listed in the file in the top level folder: `reading-measures_definitions.md`.

Can be recreated using this script: ``preprocessing_scripts/compute_reading_measures.py``.

## rm_word_features

This folder contains the eye-tracking data for each reader and each text **sequentially ordered by word order in the
text**.
It merges the information in the `reading_measures` folder with text and word features and information about the reader and
the experiment.

Can be (re)created using this script: ``additional_scripts/merge_reading_measures+word_features.py``.

## scanpaths

This folder contains the eye-tracking data for each reader and each text **temporally ordered by fixation**.

The scanpaths can be (re)created using this script: ``additional_scripts/merge_fixations+word+char.py``.


**NOTE**: the files can be easily merged with the reader information using this script 


## File: ``fixation_data_all_readers.csv``
I don't remember what this is and how it is created...

## File: ``FixRep_20_Mai_2017.txt``
Original fixation report from created from the Data Viewer.

