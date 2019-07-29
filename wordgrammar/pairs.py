'''
Defines a series of observed word-pairs in
the corpus which are used for distinguishing
ambiguous cases.
'''

import collections
from positions import Positions

class Conjunction:
    '''
    Assembles attested conjunction word-pairs in BHSA.
    Returns a dict mapping from a word to all its pairs.
    '''
    
    def __init__(self, tf):
        
        self.tf = tf
        F = tf.api.F
        
        covered = set() # skip items already matched
        self.pairs = collections.defaultdict(set)
    
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

    def conj_climber(self, a):
        '''
        Climbs down conjunction chains recursively
        and yields the connected words. Start with first word.
        '''
        F = self.tf.api.F

        yield a

        P = Positions(a, 'phrase', self.tf).get
        subs = {'subs', 'nmpr', 'adjv'}

        # define set of potential conjunction positions
        b = (
            (P(2) 
                 if P(1,'sp') == 'conj'
                 and P(2,'sp') != 'art'
                 and P(2,'sp') in subs 
                 else None)

            or (P(3)
                    if P(-1,'sp') == 'art' 
                    and P(1,'sp') == 'conj'
                    and P(2,'sp') == 'art' 
                    and P(3,'sp') in subs 
                    else None)

            or (P(3) 
                    if P(-1,'sp') == 'prep' 
                    and P(1,'sp') == 'conj'
                    and P(2,'sp') == 'prep' 
                    and P(3,'sp') in subs 
                    else None)

            or (P(4)
                    if P(-1,'sp') == 'art' 
                    and P(-2,'sp') == 'prep' 
                    and P(1,'sp') == 'conj'
                    and P(2,'sp') == 'prep'
                    and P(3,'sp') == 'art'
                    and P(4,'sp') in subs
                    else None)
            )

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