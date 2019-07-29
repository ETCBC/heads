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
from quantifiers import Quants
from prepositions import Preps
from pairs import Conjunction, Construct
#from accents import Disjoint

class WordSets:
    '''
    Delivers word sets by executing
    their respective scripts.
    '''
    def __init__(self, tf, silent=True):
        self.silent = silent
        
        self.report('processing quants...')
        self.quants = Quants(tf).quants
        self.report('\tdone')
        
        self.report('processing preps...')
        self.preps = Preps(tf).preps
        self.report('\tdone')
        
        self.report('processing conjunctions...')
        self.conjpairs = Conjunction(tf).pairs
        self.report('\tdone')
        
        self.report('processing constructs...')
        self.constpairs = Construct(tf).pairs
        self.report('\tdone')
            
        #self.accents = Accents(tf)
        #self.sim = Sim(tf).get
        
    def report(self, mssg):
        if not self.silent:
            print(mssg)