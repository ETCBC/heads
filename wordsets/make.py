'''
Constructs the word sets and pickle-zips them.
'''

import pickle
from tf.app import use
from wordsets import WordSets

output = 'wsets.pickle'

# set up TF 
print('Setting up Text-Fabric...')
A = use('bhsa', hoist=globals(), silent=True)
print('\tdone...')

print('-- RUNNING WORDSETS --')
wsets = WordSets(A, silent=False)
print('-- WSETS COMPLETE --')

print('Pickeling word sets...')
export = {
    'preps': wsets.preps,
    'quants': wsets.quants,
    'accent_type': wsets.accents.accenttype,
    'conj_pairs': wsets.conj.pairs,
    'cons_pairs': wsets.cons.pairs,
         }

pickle.dump(export, open('wsets.pickle', 'wb'))

print('!*!*!*! DONE !*!*!*!')