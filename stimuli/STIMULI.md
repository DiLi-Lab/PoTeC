# Stimuli
The stimuli texts are 12 German texts from undergraduate-level biology and physics textbooks (six each). All texts were edited to be approximately 150 words long (min 126, max: 180, mean: 158). Minor adjustments were made if necessary as mathematical formulas, tables and figures were deleted.

## Stimuli
For each text, three text comprehension questions and three background questions were created. The text comprehension questions required a thorough understanding of the text, but did not require any additional background knowledge. The background questions, in contrast, tested the general knowledge in the topic presented in the text and hence required background knowledge.

All texts and questions for each text are contained in [stimuli.tsv](./stimuli/stimuli.tsv). 

In addition, the texts and corresponding questions are also provided as separate text files in the [biology texts](./stimuli/bio_texts) and 
[physics texts](./stimuli/physics_texts) folder. 

> Refer to the [CODEBOOK](../CODEBOOK.md) for more information.

### Stimuli Sources

The sources for the stimuli texts are found in the `stimuli.bib` file and below.

#### Biology texts
**b0**: Ableitner, O. (2014). Einführung in die Molekularbiologie. Basiswissen für das Arbeiten im Labor. Wiesbaden: Springer.

**b1**: Graw, J. (2015). Genetik (6th ed.). Berlin: Springer.

**b2**: Townsend, C.R., Begon, M., Harper, J.L. (2003). Ökologie (J. Steidle, F. Thomas, B. Stadler, U. Hoffmeister, & T. Hoffmeister, Trans.). Berlin: Springer.

**b3, b4, b5**: Boujard, D., Anselme, B., Cullin, C., Raguénès-Nicol, C. (2014). Zell- und Molekularbiologie im Überblick (S. Lechowski, Trans.). Berlin: Springer.

#### Physics texts
**p0, p1, p3**: Demtröder, W. (2014). Experimentalphysik 4: Kern-, Teilchen- und Astrophysik (4th ed.). Berlin: Springer.

**p2, p4**: Demtröder, W. (2009). Experimentalphysik 2: Elektrizität und optik (5th ed.). Berlin: Springer.

**p5**: Demtröder, W. (2010). Experimentalphysik 3: Atome, Moleküle und Festkörper (4th ed.). Berlin: Springer.




## Items
Participants received different versions of the stimuli. Version numbers are specified in the data files. Item versions
differ:
* in the order of the texts
* in the order of the _answer options_ of each question

Questions are always ordered the same with text questions coming first and background questions coming second.

All different items are specified in the [items.csv](./stimuli/items.tsv) file.

> Refer to the [CODEBOOK](../CODEBOOK.md) for more information.

## AOI texts
For each of the 12 stimuli texts there is an `.ias` file that contains the areas-of-interest (AOI). AOIs are specified as character indices in the text and are defined as a rectangle around each character. Those files have been automatically created by the SR Research Data Viewer Software.
Interest areas for questions are deleted. 
Quotes symbols are replaced by * (for csv reader to open without regexp problems).
No other changes were made to these files.

> Refer to the [CODEBOOK](../CODEBOOK.md) for more information.

## Word features
Please see the ANNOTATIONS.md file for more information on the word features and how they were created.

## Practice texts
All participants received the same practice text before the real experiment started. 
The practice texts are contained in the [practice items](./practice_items.txt) file.






	
