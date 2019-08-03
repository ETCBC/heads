'''
Classes that collect data on the grammatical 
environment surrounding a given node.
'''

from positions import Positions, Getter

def getnext(condict):
    '''
    Evaluates a condition dict and 
    returns first valid item.
    '''
    results = [pos for pos, conds in conddict.items 
                   if all(conds.values())]
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
    
    def __init__(self, n, tf, **wsets):
        quants = wsets['quants'] # word sets
        preps = wsets['preps']
        P = Positions(n, 'phrase_atom', tf).get
        self.kids = {}
        self.explain = {}
        
        # set up vars
        self.P = P
        self.quants = quants
        self.preps = preps
        conddict = self.conddict
        
        # RETRIEVE RELATIONSHIPS
        
        # -- construct patterns --        
        const = {
                P(1): conddict(
                    "P(0,'st') == 'c'",
                    "P(1,'sp') != 'art'",
                ),
            
                P(2): conddict(
                    "P(0,'st') == 'c'",
                    "P(1,'sp') == 'art'",
                ),
        }
        
        self.kids['const'] = getnext(const)
        self.explain['const'] = const
    
        # -- adjacency patterns --
        # NB: a subset of these are adjectives, but 
        # this pattern does not yet parse down to that level.
        
        nominals = {'subs', 'nmpr', 'adjv', 'advb', 
                    'prde', 'prps', 'prin', 'inrg'}
        
        # -- kid
        adja = {
            P(1): conddict(
                "P(1,'sp') in nominals",
                "P(1,'nu') == P(0,'nu')",
                "P(0,'st') == 'a'",
            ),
            
            P(1): conddict(
                "P(1,'sp vt').issubset({'verb', 'ptcp', 'ptca'})",
                "P(1,'nu') == P(0,'nu')",
                "P(0,'st') == 'a'",
            ),
            
            P(2): conddict(
                "P(1,'sp') == 'art'",
                "P(2,'sp') in nominals",
                "P(2,'nu') == P(0,'nu')",
                "P(0,'st') == 'a'",
            ),
        }
        
        self.kids['adja'] = getnext(adja)
        self.explain['adja'] = adja
        
        # -- preposition mods -- 
        # NB: noun + prep NOT prep + noun
        
        prep = {
            P(1): conddict(
                "P(1) in preps"
            )
        }
        
        self.kids['prep'] = getnext(prep)
        self.explain['prep'] = prep
        
        # -- coordinate patterns -- 
        # NB: kid == thismom AND thatkid
        
        coord = {
    
            P(2): conddict(
                "P(1,'sp') == 'conj'",
                "P(1, 'sp') in nominals",
            ),
            
            P(3): conddict(
                "P(1,'sp') == 'conj'",
                "P(2, 'sp') == 'art'",
            ),
            
            P(3): conddict(
                "P(1,'sp') == 'conj'",
                "P(2) in preps",
                "P(3,'sp') in nominals",
                "P(-1) in preps",
            ),
            
            P(4): conddict(
                "P(1,'sp') == 'conj'",
                "P(2) in preps",
                "P(3,'sp') == 'art'",
                "P(-1, 'sp') == 'art'",
                "P(-2) in preps",
            ),
        }
        
        self.kids['coord'] = getnext(coord)
        self.explain['coord'] = coord
    
        # -- quantifier patterns --
        quant = {
            
            P(1): conddict(
                "P(0) not in quants",
                "P(1) in quants",
            ),

            P(2): conddict(
                "P(0) not in quants",
                "P(2) in quants",
                "P(1,'sp') == 'art'",
            ),

            P(-1): conddict(
                "P(0) not in quants",
                "P(-1) in custom_quants",
            ),
            
            P(-2): conddict(
                "P(0) not in quants",
                "P(-2) in quants",
                "P(-1,'sp') == 'art'",
            ),
        }
        
        self.kids['quant'] = getnext(quant)
        self.explain['quant'] = quant
        
    def conddict(self, *conds):
        '''
        Convert string arguments to string:eval(string) dict.
        '''
        P = self.P
        quants = self.quants
        preps = self.preps
        return {cond:eval(cond) for cond in conds}