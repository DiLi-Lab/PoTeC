# Stimuli
The stimuli text and the comprehension questions are contained in this folder. 
More detailed information on the content of the files (e.g. column names and data types) is found in the [codebook](./CODEBOOK.md).

## Texts and questions
All text and questions are contained in a [csv-file](./texts_and_questions.csv). In addition, the texts are also provided as separate text files in the [texts](./texts) folder. 
With all of the questions listed.

### Sources



## Text tags

## Word features




## ----------- text below: check what needs to go to README from 'notes.txt' ----------------


Bei mapping mit rois: Interpunktion ist NICHT teil einer ROI! Leerzeichen sind auch NICHT Teil einer roi!


Tagging:
STTS Tags
Außerdem:
[-TT or TTT-Abbr-Punct-SentEnd] 
TT/TTT: Technical Term: 
	TT: allgemein verständlicher FAchausdruck
	TTT: nicht allgemein verständlicher FAchausdruck	
=> in skript wird TT zu 1, und TTT zu 2; wenn kein technical term zu 0

Abbr: 
	1: Word is an abbreviataion: z.B. RecA
	2: Word contains abbreviation: DNA-Fragment

später umbenannt in binäres Feature: isAbbr und containsAbbr

Quote: word is inside an expression that is in quotation marks 


TODO
" wird als [$(] getaggt 
( wird als [$(] getaggt 
QuotBegin/QuotEnd raus
Paren: word is inside an expression/passage that is in parenthesis		
TODO in skript: itemId s sollen b0,-b5 bzw. p0-p5 sein	
	
	
Hyph: Word with hyphen inside DNA-Fragment; UV-Licht, z-Richtung, Calcium-Ionen (*nicht* Wörter, die Tag TRUNC (Kompositions-ERstglieg) haben); β-D-Glucose
Symb: contains symbol, z.B. z-Richtung, +Ende; β-D-Glucose


DlexDB:
passenden posTag eintrag gewaehlt; manchmal dlex nicht korrekt getaggt, dann denjenigen tag ausgewählt, der wohl der passende ist (adja beid beide +nn oder adv bei daher obwohl es eigentlich pav ist.
Schwesterchromatide: dlex: prels; => so gelassen.
Ligation=> ptkvz
==> um derartige Wörter zu finden: mein Postag mit dlexdb postag vergleichen. => wenn nicht gleich, dann ggf problematischer eintrag, bzw. in dlexdb nicht vorhanden.
fuer alle eintraege geprüft, ob sie auf richtiges Lemma gemappt wurden; ggf missing values eingefuegt;
eintraege mit richtigem postag ausgewaehlt; da in dlexdb aber tagging errors sind, alle einträge semi-manuell durchgegangen und fuer jeden eintrag, wo mein tag nicht dem von dlexdb vergegebenen tag entspricht, entschieden, was tun. 
lemma, silben, silbenzahl, worlaenge, lemmalaenge fuer in dlexdb fehlende woerter manuell ergaenzt;
in dlexeintraegen, mapping zu lemma geprüft. wenn falsches lemma, dann entsprechende eintraege gelosescht (lemma-laenge, lemma-frequenz etc)


TODO: Abkürzungen haben Silben: None; typelengthSyllables: None
TODO: Woerten mit Symb: silben nur dann, wenn eindeutig. zb: z-richtung; +Ende: 3 silben; dna-Fragment: none silben, in dlexdb dna als eine silbe, aber nicht gut; bzw: none (in dlex: 1 silbe, aber nicht gut; 5 silben waere aber auch nicht gut)
todo card: silben, silbenzahl none, falls zahl als ziffern gegeben z.B. 800
wenn wort zu viele absurde postags in dlex (z.B mikrotubuli), dann annotated type frequency auf none gesetzt
Wenn Lemma da, aber type nicht, dann Lemma frequency ergänzt
wenn falsch getaggt, aber eindeutig, dass einfach nur falsch getaggt (z.B. Dimer gibt es einen Eintrag, dort als pis getaggt; pis durch None ersetzt, sonst alles gelassen)
Wenn kein eintrag in Dlexdb, lemma, lemmalenght, syllables and type length in syllables manuell hinzugefügt
wenn Types viel falsch getaggt (z.B. SEkundär-), dann Annotated type freq auf None gesetzt


TODO:
prüfen, ob in allen text features dateien die header gleich sind.
	
Nur in Skript:	
	
PunctAfter:
 	The tags of the punctuation mark(s) (can be more than one) that directly follow the current word
	The word is followed by a punctuation mark
	
PunctBefore:
	
SentEnd: The word is the last word of the sentence	

Quot

	
