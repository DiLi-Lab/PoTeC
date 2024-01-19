# Additional Scripts

This directory contains all the necessary scripts that have been used to further process the data. 

> Refer to the [CODEBOOK](../CODEBOOK.md) for more information on the resulting output files.


## Computing reading measures

The script is made to compute a number of commonly used reading measures for eye-tracking research.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/compute_reading_measures.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/reading_measures``


## Generate scanpaths

Generates the scanpaths for each reader and text.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/generate_scanpaths.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/scanpaths``

## Generate syntax trees

This script generates the constituency and dependency trees for each sentence in each stimulus text.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/generate_scanpaths.py
 ```

 **Results**

 The files will be written to a newly created file ``../stimuli/dependency_trees.csv`` and ``../stimuli/constituency_trees.csv``

## Merge reading measures

Merges the reading measures for each reader and each text with the word features for each text and the information on the reader.
> Prerequisite: you need to run `compute_reading_measures.py` first.


**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/merge_reading_measures.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/reader_rm_wf``

## Merge scanpaths

Merges the scanpath for each reader and text with the reading measures, word features for each text and the information on the reader.
> Prerequisite: you need to run `compute_reading_measures.py` and `generate_scanpaths.py` first.


**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/merge_scanpaths.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/scanpaths_rm_wf``

## Compute surprisal

Scripts that are used to compute surprisal values for each word in the text.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/get_surprisal.py
 ```

 **Results**

 The script does not create any new files but merges the surprisal values with the `word_features` files contained in
 `stimuli/word_features/`.

