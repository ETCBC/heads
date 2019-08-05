'''
This module delivers a series of sets
which are needed to process word relations
and semantic heads. This includes:

    • accent classification sets
    • custom nominal sets
    • custom quantifier sets
    • custom preposition sets
    • attested coordinate pair sets
    • attested construct pair sets
    
The sets are built by querying the corpus
for matching patterns. 
'''

from accents import Accents
from nominals import Nominals
from quantifiers import Quants
from prepositions import Preps
from pairs import Conjunction, Construct

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
        
        self.report('processing nominals...')
        self.noms = Nominals(tf).nominals
        self.report('\tdone')
        
        self.report('processing quants...')
        self.quants = Quants(tf).quants
        self.report('\tdone')
        
        self.report('processing preps...')
        self.preps = Preps(tf).preps
        self.report('\tdone')
        
        base_sets = {
            'quants':self.quants,
            'preps':self.preps,
            'noms': self.noms
        }
        
        self.report('processing conjunctions...')
        self.conj = Conjunction(tf, **base_sets)
        self.report('\tdone')
        
        self.report('processing constructs...')
        self.cons = Construct(tf, **base_sets)
        self.report('\tdone')
        
        #self.sim = Sim(tf).get
        
    def report(self, mssg):
        if not self.silent:
            print(mssg)