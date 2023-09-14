# TODOs

**bold** = need to discuss!

- [ ] check if reading measures are calculated correctly and debug all scripts one more time! (they look nicer but might still produce wrong output)
- [ ] rewrite scripts such that they can be run from correct folder
- [ ] write bsh script to run all scripts in correct order with correct arguments
- [ ] add syllables to abbr e.g. dna-fragment we're doing it phonetically
- [ ] [codebook](../CODEBOOK.md)
- [ ] add table of contents to codebook
- [ ] spell check
- [ ] there is a folder [RANDOM](RANDOM) where I put all the files that I don't know what to do with, can someone check those?
- [ ] Und es fehlt auch noch Informationen zu den comprehension questions und wie sie kodiert sind. 
- [ ] for some readers we do not have accuracy values (?) --> add to the codebook missing values column which ones are missing (the raw nan count is not really informative)
- [ ] update running instructions, requirements files etc.
- [ ] --> Kannst du vielleicht auch noch eine Art Baum zeichnen, der darstellt, wie das preprocessing durchgeführt wird/wurde (also welches skript angewendet wird um dann welchen datensatz zu erzeugen)?
- [ ] fix mismatching pos tags (see stuff to check)
- [ ] layout der button box irgendwo darstellen
- [ ] Bei mapping mit rois: Interpunktion ist NICHT teil einer ROI! Leerzeichen sind auch NICHT Teil einer roi!

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

text-tags, contains_hyphen: Word with hyphen inside DNA-Fragment; UV-Licht, z-Richtung, Calcium-Ionen ; β-D-Glucose
