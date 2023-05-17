# Changelog


### 2023-05-17

- Added 2021 version
- Moved obsolete code into `old` directory
- The previous notebook code for generating the features contained a lot of manual corrections. In order to keep the code consistent between versions, I've created a stripped-down notebook that removes those manual adjustments. The goal is not 100% accuracy, but accurate for the majority of cases. Heads data should be used as a helper tool for building good data, not as a final gold standard for ML training / research. 


### 2019-12-17

- The work of selecting heads most accurately will need to rely on a new data model. The data model is currently being updated by Constantijn Sikkel. In the update below from October, I noted the experimental work I have done in working without subphrases. That effort has had good success in modeling heads as part of a larger constructional context. In my Time Collocations project, I am modeling phrases as graphs of constructions, using NetworkX to represent the graphs. For the time being, the current method of heads selection as seen in [phrase_heads.ipynb](old/phrase_heads_OBSOLETE.ipynb) is the best option, though imperfect as it may be. While the method I am using in the Time Collocations project is successful, I have also learned that it is simply too hard to model phrase structure for all phrases without a dedicated project of its own. For that reason, I direct the user to await the new data model from the ETCBC, which intends to address all of the problems that I have worked to outline in this repository. 

### 2019-09-30

- A new method for selecting heads, begun in July 2019 and seen in [going_subphraseless.ipynb](going_subphraseless.ipynb) is now being carried out in a separate repository ([here](https://github.com/CambridgeSemiticsLab/BH_time_collocations)). Eventually after that work has complete, I intend to transfer the methods used there to this repository. But for now I must continue the work under the rubric of my current PhD thesis. 

