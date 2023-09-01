# PoTeC Eye-tracking Data

The eye-tracking data is provided in different formats which are explained in this README. The folders are named
accordingly.
One file always contains the data for one reader and one text and is named according to this scheme:
`reader[reader_id]_[text_id]_[data_suffix].txt`.
"data_suffix" refers to the specific data format.

## raw_data
The raw data in readable ``.asc`` format. The originally generated ``.edf`` files were converted to ``.asc`` using the
SR Research `edf2asc` tool.


## fixations

Each file contains the fixations for each word in each text.

>Fixations and saccades were computed from the raw data using the Eyelink Data Viewer software package provided by SR 
Research with the default parameter settings \citep{dataviewer}. Subsequently, each fixation  was mapped to the 
character in the text that was fixated, the original screen coordinates (in pixels) were discarded. Fixations on the 
white space between two words were mapped to the closest character. Visual inspection of the data revealed that in 
certain fixation sequences, vertical calibration error gradually increased over time. This measurement error was 
semi-automatically corrected by adjusting the fixation-to-character mapping (i.e., re-mapping a fixation to the 
character in the line above or below the currently mapped character).

There files are obtained by splitting the fixation report (`OSF/eyetracking_data/FixRep_20_Mai_2017.txt`) produced 
by the Data  using this script: `OSF/preprocessing/split_fixation_report.py`. NOTE: the fixations were 
manually corrected using an unpublished script. The script adds new columns that are now 
in the fixations files in this folder ("line", "index_inline", "ORIGINAL_CURRENT_FIX_INDEX", "Fix_adjusted"). 
If the fixation report is split again using the splitting script these columns 
will be missing!

## reading_measures

> From the fixation data, various reading measures commonly used in reading research were computed 
(see `compute_reading_measures.py`). Each word (defined by the surrounding white spaces) was considered one 
region of interest for all measures except for landing position which was based on the characters within a word. 
Fixations on the punctuation marks were considered to belong to the preceding word by default and to the following 
word in case of opening parentheses or opening quotation marks. Definitions of the various measures are provided in 
Table~\ref{tab:em}. Note that several of these measures are linearly dependent. 

Each file in this folder contains the reading measures for each word in each text. The data suffix for these files is "
rm". All the reading measure and their definitions are listed in the file in the top level folder: `reading-measures_definitions.md`.

Can be recreated using this script: ``preprocessing_scripts/compute_reading_measures.py``.

## reader_rm_wf

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
Original fixation report created from the Data Viewer.

