'''
Classes that collect data on the grammatical 
environment surrounding a given node.
'''

from positions import Positions, Getter, Evaluator

def get_quantified(word, tf, **wsets):
    '''
    Recursively calls down a quantifier chain until
    finding a quantified word.
    '''
    
    quants, noms = wsets['quants'], wsets['noms']

    P = Positions(word, 'phrase_atom', tf).get

    target = (
        lambda n: P(n), 
        lambda n: P(n) not in quants,
        lambda n: P(n, 'sp') in noms,
    )

    # check this word
    if all(cond(0) for cond in target):
        return word
    
    # check next word
    elif all(cond(P(1)) for cond in target):
        return P(1)
    
    # move up one
    else:
        return get_quantified(P(1))

def getnext(ctuple):
    '''
    Returns first valid node from a {node:{string:boolean}} dict
    where all booleans must == True.
    '''
    results = [pos for pos, conds in ctuple if all(conds.values())]
    return Getter(results)[0]
    
class Mom:
    '''
    Identifies syntactic "relations"*
    from a word to its goverened elements.
    This class thus returns nodes that are 
    DEPENDENT on the mother (this node).
    
    Conditions are stored as strings and converted
    to booleans in order to easily diagnose why certain 
    items are validated.
    
    * the term "relation" is used loosely to
    refer to recurring noun patterns of modification.
    These patterns reflect productive constructions.
    '''
    
    def __init__(self, n, tf, **kwargs):
        quants = kwargs['quants'] # word sets
        preps = kwargs['preps']
        nominals = kwargs['noms']
        self.context = kwargs.get('context', 'phrase_atom')
        
        # set up variables needed for processing / storing
        P = Positions(n, self.context, tf).get
        quants = quants
        preps = preps
        self.P = P
        self.kids = {}
        self.explain = {}
        
        # set up evaluator with namespace as is
        # NB: Evaluator will rely on variables in
        # __init__, including P, quants, and preps
        self.conddict = Evaluator(locals()).conddict
        
    def analyze(self):
        '''
        Store ALL relationships.
        '''
        self.construct()
        self.adjacency()
        self.prep_mod()
        self.coordinate()
        self.quantifiers()

    def construct(self):
        '''
        Finds construct relations.
        '''
        P = self.P
        conddict = self.conddict

        const = (
                (P(1), conddict(
                    "P(0,'st') == 'c'",
                    "P(1,'sp') != 'art'",
                )),

                (P(2), conddict(
                    "P(0,'st') == 'c'",
                    "P(1,'sp') == 'art'",
                )),
        )

        self.kids['const'] = getnext(const)
        self.explain['const'] = const
        return getnext(const)

    def adjacency(self):
        '''
        Find adjacent nominals to this word.
        NB: a subset of these are so-called adjectives, but 
        this pattern does not yet parse down to that level.
        '''
        P = self.P
        conddict = self.conddict
        
        adja = (
            (P(1), conddict(
                "P(1) in nominals",
                "P(0,'st') == 'a'",
            )),

            (P(2), conddict(
                "P(1,'sp') == 'art'",
                "P(2) in nominals",
                "P(0,'st') == 'a'",
            )),
        )

        self.kids['adja'] = getnext(adja)
        self.explain['adja'] = adja
        return getnext(adja)

    def prep_mod(self):
        '''
        NB: noun + prep NOT prep + noun
        '''
        P = self.P
        conddict = self.conddict

        prep = (
            (P(1), conddict(
                "P(1) in preps"
            )),
        )

        self.kids['prep'] = getnext(prep)
        self.explain['prep'] = prep
        return getnext(prep)

    def coordinate(self):
        '''
        gets coordinate patterns
        NB: kid == thismom AND thatkid
        '''
        P = self.P
        conddict = self.conddict

        coord = (

            (P(2), conddict(
                "P(0) not in preps",
                "P(1,'sp') == 'conj'",
                "P(2) in nominals",
                "P(2) not in preps"
            )),

            (P(3), conddict(
                "P(0) not in preps",
                "P(1,'sp') == 'conj'",
                "P(2,'sp') == 'art'",
            )),

            (P(3), conddict(
                "P(1,'sp') == 'conj'",
                "P(2) in preps",
                "P(3) in nominals",
                "P(-1) in preps",
            )),

            (P(4), conddict(
                "P(1,'sp') == 'conj'",
                "P(2) in preps",
                "P(3,'sp') == 'art'",
                "P(-1,'sp') == 'art'",
                "P(-2) in preps",
            )),
        )

        self.kids['coord'] = getnext(coord)
        self.explain['coord'] = coord
        return getnext(coord)

    def quantifiers(self):
        '''
        -- quantifier patterns --
        '''
        P = self.P
        conddict = self.conddict

        quant = (

            (P(1), conddict(
                "P(0) not in quants",
                "P(1) in quants",
            )),

            (P(2), conddict(
                "P(0) not in quants",
                "P(2) in quants",
                "P(1,'sp') == 'art'",
            )),

            (P(-1), conddict(
                "P(0) not in quants",
                "P(-1) in quants",
            )),

            (P(-2), conddict(
                "P(0) not in quants",
                "P(-2) in quants",
                "P(-1,'sp') == 'art'",
            )),
        )

        self.kids['quant'] = getnext(quant)
        self.explain['quant'] = quant
        return getnext(quant)