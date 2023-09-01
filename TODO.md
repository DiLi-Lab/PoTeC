# TODOs

**bold** = need to discuss!

- [ ] check if reading measures are calculated correctly
- [ ] **all labels are encoded the same (e.g. expert is now sometimes E and sometimes 0 or 1)**
    - [ ] expert / non-expert
    - [ ] gender
    - [ ] 
- [ ] **encoding of nan / missing values (sometimes nan, sometimes . or something)**
- [ ] check data types in code book and rename, so far created automatically from csv
- [ ] [codebook](./CODEBOOK.md)
    - [ ] remove duplicate column names, e.g. word features or text tags and reference to the table where they are defined (text_id and item_id, word_index_sent and word_index_in_sent)
    - [ ] look at todos in codebook --> for some data files there are todos
    - WORD_INDEX --> what is it? word index in text probably
    - [ ] **all column headers should be the same in all data files (good & informative names)**
      - [ ] I started adding name suggestions in the codebook in the column name column. the name after the semicolon (:) is my suggestion
      - [ ] camel case or underscores?
      - [ ] decide for capitalization? sometimes all caps, sometimes camel case, sometimes weird...
- [ ] delimiters! all should be the same, it is a mix between 4 spaces and tab (comma?) --> make all tabs
- [ ] add table of contents to codebook
- [ ] debug all scripts one more time! (they look nicer but might still produce wrong output)
- [ ] spell check
- [ ] remove duplicate columns in data files --> sometimes because of different column names, the same column is in there twice
- [ ] (uncorrected) fixation data: is the value of the RECORDING_SESSION_LABEL column always identical to the reader-ID in the filename?]
- [ ] **data annotation readme!** --> check [ANNOTATION](./stimuli/ANNOTATION.md) --> I am not sure if we need this or if we should include it in the codebook...
- [ ] what is the difference between word features and text tags files? can we merge them?
- [ ] there is a folder [RANDOM](./RANDOM) where I put all the files that I don't know what to do with, can someone check those?
- [ ] check the questions and put them into a csv file and note down in the readme that they are in the txt files + separately in csv
- [ ] Und es fehlt auch noch Informationen zu den comprehension questions und wie sie kodiert sind. 
- [x] ~~what can we directly copy from the paper? (e.g. the description of the reading measures) --> do we need to cite this if we copy it literally? or should I just refer to the corresponding section in the paper? so far all direct quotes that I put in the readmes are indented in a block~~
