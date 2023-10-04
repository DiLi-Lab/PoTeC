# Additional Scripts

<mark>TODO: finish/fix this file</mark>

This directory contains all the necessary scripts that can be used to further process the data. All scripts described below can be run in the correct order using this script: TODO!

> Refer to the [CODEBOOK](../CODEBOOK.md) for more information on the resulting output files.


## `compute_reading_measures.py`
The script is made to compute a number of commonly used reading measures for eye-tracking research.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/compute_reading_measures.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/reading_measures``


## ```generate_scanpaths.py```

Generates the scanpaths for each reader and text.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/generate_scanpaths.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/scanpaths``

## ``merge_rm_wf.py``

Merges the reading measures for each reader and each text with the word features for each text and the information on the reader.
> Prerequisite: you need to run `compute_reading_measures.py` first.

**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/merge_rm_wf.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/reader_rm_wf``

## `merge_scanpaths_rm_wf.py`

Merges the scanpath for each reader and text with the reading measures, word features for each text and the information on the reader.
> Prerequisite: you need to run `compute_reading_measures.py` and `generate_scanpaths.py` first.


**How to run:**
 ```bash
 # python or python3
 python [path_to_additional_scripts]/merge_scanpaths_rm_wf.py
 ```

 **Results**

 The files will be written to a newly created folder ``../eyetracking_data/scanpaths_rm_wf``

