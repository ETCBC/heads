'''
Delivers custom prepositions.
'''

class Preps:
    
    def __init__(self, tf):
        
        # prepare prepositions set

preps = [w for w in F.otype.s('word') if F.pdp.v(w) == 'prep']

# add special בד "alone" when it is 
# preceded by ל, with a meaning of "except"
preps.extend(A.search('''

prep:word lex=BD/
/with/
phrase_atom
    word pdp=prep lex=L
    <: prep
/-/

''', shallow=True, silent=True))

# The prepositions below are lemma sets like פנה or תוך
# These sets could benefit from further investigation
preps.extend(A.search('''

prep:word prs=absent lex=PNH/|TWK/|QY/|QYH=/|QYT/|<WD/
/with/
% ensure potential prep is preceded by:
% prep, potential prep (ls), or כל
% else there should be no interruption
phrase_atom
    word
    /with/
    pdp=prep
    /or/
    ls=ppre
    /or/
    lex=KL/
    /-/
    <: prep
/-/
/with/
% ensure prep is followed by at least one non ו word
phrase_atom
    prep
    <: word lex#W
/-/

''', shallow=True, silent=True))

# several cases of אחרית are substantive in nature, e.g. אחרית רשׁעים "end of evil doers" (Ps 37:38)
# others are used prepositionally to indicate position
# the semantics of the phrase is important for determining which sense is employed
# all cases in Time Phrases appear prepositional
# if used with an animate noun, it appears that אחרית is used substantivally
# those cases can be manually excluded with a lexeme exclusion
# NB: גים in Jer 50:12 is used non-personally and thus not excluded
# Excluded: איוב and רשעים
preps.extend(A.search('''

prep:word lex=>XRJT/
/with/
phrase_atom
    prep
    <mother- subphrase rela=rec
        word pdp=subs lex#>JWB/|RC</
/-/

''', shallow=True, silent=True))

# Below potential preps are added, but דרך is excluded
# since this is a more speculative preposition
preps.extend(A.search('''

word ls=ppre st=c lex#DRK/

''', shallow=True, silent=True))

print(f'{len(preps)} custom prepositions ready...')