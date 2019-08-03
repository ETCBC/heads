'''
Defines a series of observed word-pairs in
the corpus which are used for distinguishing
ambiguous cases.
'''

import collections
from positions import Positions
from context import Mom

class Conjunction:
    '''
    Assembles attested conjunction word-pairs in BHSA.
    Returns a dict mapping from a word to all its pairs.
    '''
    
    def __init__(self, tf, **wsets):
        
        self.tf = tf
        F = tf.api.F
        quants = wsets['quants'] # wordsets
        preps = wsets['preps']
        covered = set() # skip items already matched
        self.pairs = collections.defaultdict(set)
        self.pairresults = collections.defaultdict(lambda:collections.defaultdict(list))
    
        # gather pairs
        for w in F.otype.s('word'):

            # skip words already visited in a chain
            if w in covered:
                continue

            # check for chain
            chain = list(self.conj_climber(w))
            if not chain:
                continue

            # add pairs
            for i in chain:
                for j in chain:
                    if i == j:
                        continue
                    self.pairs[F.lex.v(i)].add(F.lex.v(j))
                    self.pairresults[F.lex.v(i)][F.lex.v(j)].append((i, j))

    def conj_climber(self, a):
        '''
        Climbs down conjunction chains recursively
        and yields the connected words. Start with first word.
        '''
        F = self.tf.api.F

        yield a

        P = Positions(a, 'phrase', self.tf).get
        subs = {'subs', 'nmpr', 'adjv'}

        b = 

        if b:
            yield from self.conj_climber(b)
            
class Construct:
    '''
    Collects all potential goverened
    construct pairs, where key is in
    construct state and value is a set
    of valid goverened genitives.
    '''
    
    def __init__(self, tf):
        
        F = tf.api.F
        self.pairs = collections.defaultdict(set)
        self.pairresults = collections.defaultdict(lambda:collections.defaultdict(list))
        
        for word in set(F.otype.s('word')) & set(F.st.s('c')):
        
            P = Positions(word, 'verse', tf).get
        
            # Set up potential construct position
            construct = (
                P(1)
                    if P(1, 'sp') != 'art'
                    else None
                or P(2)
                    if P(1, 'sp') == 'art'
                    else None
            )
            
            if not construct:
                continue
                
            self.pairs[F.lex.v(word)].add(F.lex.v(construct))
            self.pairresults[F.lex.v(word)][F.lex.v(construct)].append((word, construct))