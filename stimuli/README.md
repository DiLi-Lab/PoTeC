# Stimuli
The stimuli text and the comprehension questions are contained in this folder. 
More detailed information on the content of the files (e.g. column names and data types) is found in the [codebook](./CODEBOOK.md).

## Stimuli
All text and questions are contained in a [csv-file](./stimuli/stimuli.csv). 

TODO: decide whether we want to do have this:
In addition, the texts and corresponding questions are also provided as separate text files in the [biology texts](./stimuli/bio_texts) and 
[physics texts](./stimuli/physics_texts) folder. 

### Stimuli Sources
TODO: add list of sources and which text is from what book and what pages etc.

## Items
Participants received different versions of the stimuli. Version numbers are specified in the data files. Item versions
differ:
* in the order of the texts
* in the order of the _answer options_ of each question

Questions are always ordered the same with text questions coming first and background questions coming second.

All different items are specified in the [items.csv](./stimuli/items.csv) file.

## AOI texts
Specified the areas-of-interests for all stimuli texts. AOIs are specified as character indices in the text.
Interest areas for questions are deleted. 
Quotes are replaced by * (for csv reader to open without regexp problems)
No other changes were made to these files.

## Word features
Please see the ANNOTATIONS.md file for more information on the word features and how they were created.

## Practice texts
All participants received the same practice texts before the real experiment started. 
The practice texts are contained in the [practice items](./practice_items.txt) file.






	
