# TODOs

**bold** = need to discuss!

- [ ] check if reading measures are calculated correctly and debug all scripts one more time! (they look nicer but might still produce wrong output)
- [ ] rewrite scripts such that they can be run from correct folder
- [ ] write bsh script to run all scripts in correct order with correct arguments
- [ ] **all labels are encoded the same (e.g. expert is now sometimes E and sometimes 0 or 1)**
- [ ] add syllables to abbr e.g. dna-fragment we're doing it phonetically
- [ ] [codebook](./CODEBOOK.md)
    - [ ] remove duplicate column names, e.g. word features or text tags and reference to the table where they are defined (text_id and item_id, word_index_sent and word_index_in_sent)
    - [ ] look at todos in codebook --> for some data files there are todos
    - [ ] see `new_col_mapping.csv` --> I put all the new columns names in there, all that are NOT in there will remain the same, those that do not have a new name, will simply be lowercased but nothing else
- [ ] add table of contents to codebook
- [ ] spell check
- [ ] remove duplicate columns in data files --> sometimes because of different column names, the same column is in there twice
- [ ] there is a folder [RANDOM](./RANDOM) where I put all the files that I don't know what to do with, can someone check those?
- [ ] Und es fehlt auch noch Informationen zu den comprehension questions und wie sie kodiert sind. 
- [ ] [error log files](preprocessing_scripts/rm_error_log.txt), delete
- [ ] merge this [rm definition](reading-measures_definitions.md) with Codebook
- [ ] for some readers we do not have accuracy values (?) --> add to the codebook missing values column which ones are missing (the raw nan count is not really informative)
- [ ] clean contains and is abbr --> is_abbr sollte nur 1 sein wenn es ein abbr ist, contains_abbr sollte 1 sein wenn es ein abbr enthält (but check first if true)
- [ ] update running instructions, requirements files etc.
- [x] ~~participants file: alle buchstaben ausschreiben, group hier definieren,~~ 
- [x] ~~all column headers should be the same in all data files (good & informative names)~~
  - [X] ~~camel case or underscores? --> underscores!~~
  - [x] ~~decide for capitalization? sometimes all caps, sometimes camel case, sometimes weird...~~ --> all lowercase, except tags and rm
- [x] ~~**data annotation readme!** --> check [ANNOTATION](./stimuli/ANNOTATION.md) --> I am not sure if we need this or if we should include it in the codebook...~~ --> keep it but only for notes on the process
- [x] ~~delimiters! all should be the same, it is a mix between 4 spaces and tab (comma?)~~ --> make all tabs
- [x] ~~what is the difference between word features and text tags files? can we merge them?~~ --> yes
- [x] ~~im paper und auch sonst wo steht, dass ihr tags provided für sentence and clause end, aber der tatsächliche tag heisst sentence beginning or clause beginning, wo ist der fehler?~~ --> is beginning
- [x] ~~all files are now renamed to `.csv` with tab separator! want to name them `.tsv`?~~ --> yes
- [x] ~~check the questions and put them into a csv file and note down in the readme that they are in the txt files + separately in csv~~
- [x] ~~one possibility is to leave it as a readable value (e.g. expert and beginner) in the **participants file** such that this is easy to udnerstand, but in ALL other files we can encode it numerically and specify accordingyl~~
- [x] ~~(uncorrected) fixation data: is the value of the RECORDING_SESSION_LABEL column always identical to the reader-ID in the filename?]~~
- [x] ~~**encoding of nan / missing values (sometimes nan, sometimes . or something)**~~ --> replace all missing values with string NA
- [x] ~~what can we directly copy from the paper? (e.g. the description of the reading measures) --> do we need to cite this if we copy it literally? or should I just refer to the corresponding section in the paper? so far all direct quotes that I put in the readmes are indented in a block~~


old notes:
* TODO
    * " wird als [$(] getaggt 
    * ( wird als [$(] getaggt 

## descriptions for codebook
copy these later to codebook description col once the col names are final!!!

text_tags, word length: word length in number of characters without sentence punctuation at the end (i.e., z.B. = 4 characters; DNA-Kette =9 characters; [He] eats.=4 characters

text_Tag, technical term: 
    TT: allgemein verständlicher FAchausdruck --> encoded as 1
    TTT: nicht allgemein verständlicher FAchausdruck --> encoded as 2
    if neither encoded as 0
    => we might change this to two separate columns, one for TT and one for TTT

text-tags, contains_hyphen: Word with hyphen inside DNA-Fragment; UV-Licht, z-Richtung, Calcium-Ionen (*nicht* Wörter, die Tag TRUNC (Kompositions-ERstglieg) haben); β-D-Glucose
