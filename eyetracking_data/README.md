# PoTeC Eye-tracking Data

The eye-tracking data is provided in different formats which are explained in this README. The folders are named
accordingly.
One file always contains the data for one reader and one text and is named according to this scheme:
`reader[reader_id]_[text_id]_[data_suffix].txt`.
"data_suffix" refers to the specific data format.

> **NOTE**: for all the data described below, refer to the CODEBOOK for a full overview of data types, distributions, etc.

## Raw data
The raw data in available in ``.tsv`` format. The originally generated ``.edf`` files were converted to ``.asc`` using the
SR Research `edf2asc` tool and then parsed to `.tsv` files containing one sample per line.

## Fixations

Fixations and saccades were computed from the raw data using the Eyelink Data Viewer software package provided by SR 
Research with the default parameter settings (SR Research Ltd. 2011). Subsequently, each fixation was mapped to the 
character in the text that was fixated, the original screen coordinates (in pixels) were discarded. Fixations on the 
white space between two words were mapped to the closest character. Visual inspection of the data revealed that in 
certain fixation sequences, vertical calibration error gradually increased over time. This measurement error was 
semi-automatically corrected by adjusting the fixation-to-character mapping (i.e., re-mapping a fixation to the 
character in the line above or below the currently mapped character). The files therefore contain the corrected data.

## Reading measures

From the fixation data, various reading measures commonly used in reading research were computed. 
Each word (defined by the surrounding white spaces) was considered one 
region of interest for all measures except for landing position which was based on the characters within a word. 
Fixations on the punctuation marks were considered to belong to the preceding word by default and to the following 
word in case of opening parentheses or opening quotation marks. Definitions of the various measures are provided in the
[CODEBOOK.md](../CODEBOOK.md). Note that several of these measures are linearly dependent.

Can be (re)created using this script: ``additional_scripts/compute_reading_measures.py``.

> More information on the script is found in the additional scripts' [README](../additional_scripts/README.md)

## Merged: reader info, word features and reading measures

This folder contains the fixation data merged with the reading measures and word features ordered by word 
order of the original stimulus.

Can be (re)created using this script: ``additional_scripts/merge_rm_wf.py``.

> More information on the script is found in the additional scripts' [README](../additional_scripts/README.md)


## Scanpaths

This scanpaths folder contains the fixation data ordered temporally by fixation index.

The scanpaths can be (re)created using this script: ``additional_scripts/generate_scanpaths.py``.

> More information on the script is found in the additional scripts' [README](../additional_scripts/README.md)


## Merged: scanpaths, reading measures, word features and reader info

The scanpath files can be easily merged with the reader information, the reading measures and the word features 
using this script `additional_scripts/merge_scanpaths_rm_wf.py`. The resulting data files will be written to the folder 
`scanpaths_reader_rm_wf`.

> More information on the script is found in the additional scripts' [README](../additional_scripts/README.md)


## File: ``original_uncorrected_fixation_report.txt``
Original fixation report created from the Data Viewer. The fixations in this report have been manually corrected.
All fixation files contained in this folder are corrected: `eyetracking_data/fixations/`.

## References

SR Research Ltd. (2011). EyeLink Data Viewer user’s manual [Computer software manual]. Mississauga, Canada. (document version 1.11.1)
