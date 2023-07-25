# Additional Scripts

<mark>TODO: finish/fix this file</mark>

This directory contains all the necessary scripts that can be used to further process the data.
They can be run from this folder if the entire OSF folder is downloaded and kept as is otherwise paths can be provided. 

## ``merge_fixations+word+char.py``
Merges the fixations files in `eyetracking_data/fixations/` with stimuli and participant information.
Output files are written to the `eyetracking_data/scanpaths/` folder if not specified differently.

If a roi (which is equivalent to CharIndexInText) cannot be mapped to a character, 
the values will be written as np.NA in the output file. All errors will be logged in a file in the errors folder.


## `merge_reading_measures+word_features.py`
Merges the reading measure files in `eyetracking_data/reading_measures/` with stimuli and participant information.
Output files are written to the `eyetracking_data/rm_word_features/` folder if not specified differently. 

## `merge_scanpaths+reader_information.py`

TODO: finish script