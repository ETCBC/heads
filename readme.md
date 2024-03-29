# Heads

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7945118.svg)](https://doi.org/10.5281/zenodo.7945118)

## [See the production notebook](https://nbviewer.jupyter.org/github/ETCBC/heads/blob/master/generate_phrase_heads.ipynb)


## Features

This project produces the following features:

### Edge Features

* `head` - an edge feature from a syntactic phrase head to its phrase node
* `obj_prep` - an edge feature from an object of a preposition to its governing preposition
* `nhead` - an edge feature from a nominal syntactic phrase head to its phrase node; handy for prepositional phrases with nominal elements contained within

### Node Features
* `sem_set` - a semantic set feature which contains the following feature values:
	* `quant` - enhanced quantifier sets
	* `prep` - enhanced preposition sets 


## Production

The features are produced in [generate_phrase_heads.ipynb](generate_phrase_heads.ipynb). This notebook is run against BHSA versions `c` and `2021`.

## Use Case

**The goal is not 100% accuracy, but accurate for the majority of cases. Heads data should be used as a helper tool for building good data, not as a final gold standard for ML training / research.**

In the current base distribution of the BHSA, there is no simple way to isolate phrase heads. The BHSA does encode relations between words by grouping them into so-called "subphrases" and then drawing relations between the subphrases. In theory, the selection of phrase heads should be as simple as selecting a word that contains no dependent subphrase relations. However, several major issues complicate the matter. First, subphrases do not capture all potential relations between words. For instance, there is no subphrase relation that connects prepositions to the objects they govern. Another limitation is that any given word can only be contained within a maximum of three subphrases, due to the outdated [ps3.p](http://www.etcbc.nl/datacreation/#ps3.p) file format which only has enough column space for three subphrase embeddings. The result is that many relations, such as attribution (encoded with [the feature `atr`](https://etcbc.github.io/bhsa/features/hebrew/c/rela)) or nomen regens/rectum (commonly know as the "construct") which would normally identify a word as a dependent descriptor word, are completely missing. Second, the way in which subphrase relations are implemented is inconsistent. Subphrase relations may connect to the wrong mother subphrase. Or the way words are grouped into subphrases may differ from phrase to phrase. The result is that one must account for a wide range of potential situations when searching for syntactic phrase heads. Third, the BHSA does not account for semantic concerns when creating the subphrase relations, most notably semantic quantification. When a noun a quantified, it is often the quantifier which is contained in an independent subphrase, while the noun is connected to it with a subphrase relation of `adj`, `atr`, or `rec`. This creates a rather complex situation for syntactic head selection: the quantifier must be bypassed, and the quantified must be selected. This means that exceptions must be made in the independency requirements for quantified nouns. Further complicating the matter, these independency requirements must be passed down the phrase, so that words which are coordinated to the quantified noun are also selected. Yet, this must all be done without selecting a truly dependent, modifying word.

## Methodology

The method used in this project primarily follows a two-pronged approach to the problems outlined above. First, words are grouped into sets that are used to enhance or navigate the problematic BHSA data. For instance, in the case of missing subphrase relations, a word can be placed into a dependent-word set (`dwords`). In the case of quantifiers, the BHSA data must be enhanced. Words like כל "all" or יתר "rest" are not marked in BHSA as quantifying lexemes. By grouping these kinds of lexemes into quantifying sets, these words can be identified as quantifiers. Some prepositional modifiers are likewise not marked as prepositions in BHSA, words like פנה when occuring in the construction לפני. These terms are also added into a custom prepositional set. In the second part, [Text-Fabric Search templates](https://annotation.github.io/text-fabric/Use/Search/) that contain numerous independency checks and logic are run using the custom sets. These searches return tuples containing the result nodes. The nodes are then mapped to their enclosing phrases in a dictionary. Finally, the results are exported using the [Text-Fabric Save method](https://annotation.github.io/text-fabric/Create/CreateTF/).

## Limitations and Edge Cases
   
The quality of heads data can only be as good as the underlying BHSA data model. In most cases, the BHSA subphrases and subphrase relations enable powerful distinctions to be made which allow for great head selections. However, in many cases, the shortcomings, inconsistency, and outdatedness of the underlying BHSA phrase model cause complications. Sometimes these complications require additional logic checks just to cover a handfull of inconsistent cases. This creates bloated and redundant code. In other cases, the data model cannot even be navigated around, due to wrong or missing relation data.

The central root of the problem lies in the subphrase object. Subphrases try to do two things, and do neither one well. They try to 1) encode relations between words, 2) encode phrases that exist below the level of top-level phrases. They fail in 1 because subphrases are not generated for all words and do not encode all possible relations. They fail on 2 because the subphrase structure is inconsistent with the encoding of other phrases in BHSA. Subphrases can contain overlapping words, but phrase atoms and phrases are adjacent. Phrases and phrase_atoms have a type value (`typ`) such as `NP` (noun phrase), `PP` (prepositional phrase), etc, which tells one which heads to expect. But subphrases do not. This leads to the ultimate problem: subphrases themselves have heads, but these heads are unretrievable because subphrases do not encode relations between words directly, and because they do not contain a type which would otherwise tell which part of speech to look for. Finally, subphrases are not always generated, or do not always enclose a full phrase. This means that there are many phrases in the Hebrew Bible which are completely missed or ignored in BHSA.

The issue of heads selection thus illuminates the need to address the inconsistencies of subphrases. Until those inconsistencies are solved, the features contained in this reposistory must be considered a best-effort with the data available. Great effort has been spent on covering as many and all edge cases as could be found within a reasonable time span (about 3 weeks of full time work). But new edge cases can always be found that is attributable to the underlying subphrase problem. In as many cases as possible, the edge cases were fixed programmatically. But in some cases this is impossible.

It is the conclusion of this project that a completely new data model is needed that addresses these issues before a completely consistent heads feature can be generated. This model should describe all phrase-internal and inter-phrase relations. It should allow for recursive embedding. And it should encode phrase data for all phrases, even those that are embedded.    
