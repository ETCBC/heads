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
#from pairs import Conjunction, Construct
from accents import Accents

class WordSets:
    '''
    Delivers word sets by executing
    their respective scripts.
    '''
    def __init__(self, tf, silent=True):
        self.silent = silent
        
        self.report('processing accents...')
        self.accents = Accents(tf)
        self.report('\tdone')
        
        self.report('processing quants...')
        self.quants = Quants(tf).quants
        self.report('\tdone')
        
        self.report('processing preps...')
        self.preps = Preps(tf).preps
        self.report('\tdone')
        
#         self.report('processing conjunctions...')
#         self.conjs = Conjunction(tf)
#         self.report('\tdone')
        
#         self.report('processing constructs...')
#         self.consts = Construct(tf)
#         self.report('\tdone')
        
        #self.sim = Sim(tf).get
        
    def report(self, mssg):
        if not self.silent:
            print(mssg)