'''
Defines a series of observed word-pairs in
the corpus which are used for distinguishing
ambiguous cases.
'''

class Pairs:
    
    def __init__(self, tf):
        
        
subs = {'subs', 'nmpr', 'adjv'}

def conj_climber(a):
    '''
    Climbs down conjunction chains recursively
    and yields the words. Start with first word.
    '''
    yield a
    
    pos = Positions(a, 'phrase')
    
    b = (
        (pos[2] if F.sp.v(pos[1])=='conj' and F.sp.v(pos[2])!='art' and F.sp.v(pos[2]) in subs else None)
    
        or (pos[3] if F.sp.v(pos[-1])=='art' and F.sp.v(pos[1])=='conj'
                and F.sp.v(pos[2])=='art' and F.sp.v(pos[2]) in subs else None)
    
        or (pos[3] if F.sp.v(pos[-1])=='prep' and F.sp.v(pos[1])=='conj'
                and F.sp.v(pos[2])=='prep' and F.sp.v(pos[3]) in subs else None)
    
        or (pos[3] if F.sp.v(pos[-1])=='art' and F.sp.v(pos[-2])=='prep' 
               and F.sp.v(pos[1])=='conj' and F.sp.v(pos[2])=='art' and F.sp.v(pos[3])=='prep'
               and F.sp.v(pos[4]) in subs else None)
        )
    
    if b:
        yield from conj_climber(b)
        

covered = set() # skip items already matched
valid_pairs = collections.defaultdict(set)

for w in F.otype.s('word'):
    
    # skip words already visited in a chain
    if w in covered:
        continue
        
    # check for chain
    chain = list(conj_climber(w))
    if not chain:
        continue
        
    # add pairs
    for i in chain:
        for j in chain:
            
#             if F.lex.v(i)=='>RY/' and F.lex.v(j) == '<WP/':
#                 raise Exception(w, chain)
            
            if i == j:
                continue
            valid_pairs[F.lex.v(i)].add(F.lex.v(j))
            
print(len(valid_pairs), 'valid pairs added...')

# expand the set

expanded_pairs = collections.defaultdict(set)

for lex, pairs in valid_pairs.items():
    for paired in pairs:
        expanded_pairs[lex] |= valid_pairs[paired]

print(len(valid_pairs), 'valid pairs added...')