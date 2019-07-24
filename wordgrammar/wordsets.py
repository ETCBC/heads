'''
This module delivers a series of sets
which are needed to process word relations
and semantic heads. This includes:

    • custom quantifier sets
    • custom preposition sets
    • valid coordinate pair sets
    • valid adjective pair sets
    
The sets are built by querying the corpus
for matching patterns. 
'''

import os
from quantifiers import get_quants
from prepositions import get_preps
...


class WordSets:
    '''
    Delivers word sets by executing
    their respective scripts.
    '''
    def __init__(self, tf):
        self.quants = Quants(tf)
        self.preps = Preps(tf)
        self.accents = Accents(tf)
        self.sim = Sim(tf).get