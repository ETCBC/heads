'''
Classes that collect data on the grammatical 
environment surrounding a given node.
'''

from positions import Positions, Getter

def conddict(*conds):
    '''
    Convert string arguments to string:eval(string) dict.
    '''
    return {cond:eval(cond) for cond in conds}

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
    
    def __init__(self, n, tf, **kwargs):
        
        tf = kwargs['tf'] # text-fabric
        wsets = kwargs['wset'] # word set
        p = Positions(n, 'phrase_atom', tf).get
        self.kids = {}
        self.explain = {}
        
        # RETRIEVE RELATIONSHIPS
        
        # -- construct patterns --        
        const = {
                p(1): conddict(
                    "p(0,'st') == 'c'",
                    "p(1,'sp') != 'art'",
                ),
            
                p(2): conddict(
                    "p(0,'st') == 'c'",
                    "p(1,'sp') == 'art'",
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
            p(1): conddict(
                "p(1,'sp') in nominals",
                "p(1,'nu') == p(0,'nu')",
                "p(0,'st') == 'a'",
            )
            
            p(1): conddict(
                "p(1,'sp vt').issubset({'verb', 'ptcp', 'ptca'})",
                "p(1,'nu') == p(0,'nu')",
                "p(0,'st') == 'a'",
            )
            
            p(2): conddict(
                "p(1,'sp') == 'art'",
                "p(2,'sp') in nominals",
                "p(2,'nu') == p(0,'nu')",
                "p(0,'st') == 'a'",
            )
        }
        
        self.kids['adja'] = getnext(adja)
        self.explain('adja') = adja
        
        # -- preposition mods -- 
        # NB: noun + prep NOT prep + noun
        
        prep = {
            
            p(1): conddict(
                "p(1, 'sp') == prep"
            
            )
            
        }
        
        prep_m = clear([ 
            
            (p(-1)
                if p(-1,'sp') == 'prep' or p(-1) in custom_preps
                else None),

            (p(-2)
                if p(-1,'sp') == 'art'
                and p(-2,'sp') == 'prep' or p(-2) in custom_preps
                else None),
        ])
        
        self.mom['prep'] = Getter(prep_m)[0]
    
        # ** coordinate patterns **
        # NB: before == mom; after == kid
        
        # -- mom
        coord_m = clear([
            
            (p(-2) 
                if p(-1,'sp') == 'conj'
                else None),

            (p(-3)
                if p(-1,'sp') == 'art'
                and p(-2,'sp') == 'conj'
                else None),

            (p(-3)
                if p(-1,'sp') == 'prep'
                and p(-2,'sp') == 'conj'
                else None),

            (p(-4)
                if p(-1,'sp') == 'art'
                and p(-2,'sp') == 'prep' or p(-2) in custom_preps
                and p(-3,'sp') == 'conj'
                else None),
        ])
        
        # -- kid
        coord_k = clear([
            
            (p(2)
                if p(1,'sp') == 'conj'
                else None),
            
            (p(3)
                if p(1,'sp') == 'conj'
                and p(2, 'sp') == 'art'
                else None),
            
            (p(3)
                if p(1,'sp') == 'conj'
                and p(2,'sp') == 'prep' or p(2) in custom_preps
                and p(3,'sp') != 'art'
                else None),
            
            (p(4)
                if p(1,'sp') == 'conj'
                and p(2,'sp') == 'prep' or p(2) in custom_preps
                and p(3,'sp') == 'art'
                else None),
            
        ])
        
        self.mom['coord'] = Getter(coord_m)[0]
        self.kid['coord'] = Getter(coord_k)[0]
    
        # ** quantifier patterns **
        
        # -- mom
        quant_m = clear([
            
            (p(-1)
                if p(0) in custom_quants
                and p(-1) not in custom_quants
                and p(-1,'sp') in {'subs', 'adjv'}
                else None),
            
            (p(-2)
                if p(0) in custom_quants
                and p(-2) not in custom_quants
                and p(-1,'sp') == 'art'
                else None),
            
            (p(1) 
                if p(0) in custom_quants
                and p(1) not in custom_quants
                and p(1,'sp') in {'subs', 'adjv'}
                else None),
            
            (p(2)
                if p(0) in custom_quants
                and p(2) not in custom_quants
                and p(1,'sp') == 'art'
                else None),
        
        ])
        
        # -- kid
        quant_k = clear([
            
            (p(1) 
                if p(0) not in custom_quants
                and p(1) in custom_quants
                and p(1,'sp') in {'subs', 'adjv'}
                else None),

            (p(2) 
                if p(0) not in custom_quants
                and p(2) in custom_quants
                and p(1,'sp') == 'art'
                and p(2,'sp') in {'subs', 'adjv'}
                else None),

            (p(-1) 
                if p(0) not in custom_quants
                and p(-1) in custom_quants
                and p(-1,'sp') in {'subs', 'adjv'}
                else None),

            (p(-2) 
                if p(0) not in custom_quants
                and p(-2) in custom_quants
                and p(-1,'sp') == 'art'
                and p(-2,'sp') in {'subs', 'adjv'}
                else None),
            
        ])
        
        self.mom['quant'] = Getter(quant_m)[0]
        self.kid['quant'] = Getter(quant_k)[0]