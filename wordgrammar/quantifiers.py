class Quants:
    
    def __init__(self, tf):
        '''
        Input: instance of Text Fabric
        Output: a series of sets containing
        custom quantifier nodes
        '''

        custom_quants = set()
        custom_quants |= set(F.ls.s('card')) & set(F.otype.s('word'))
        custom_quants |= set(F.ls.s('ordn')) & set(F.otype.s('word'))

        quant_lexs = '|'.join(['KL/', 'M<V/', 'JTR/',
                                 'M<FR/', 'XYJ/', '<FRWN/',
                                 'C>R=/', 'MSPR/', 'RB/', 'RB=/',
                                 'XMJCJT/'])
        custom_quants |= set(A.search(f'word lex={quant_lexs}', shallow=True, silent=True))

        # for the Hebrew idiom: בנ + quantifier for age
        for w in set(F.otype.s('word')) & set(F.lex.s('BN/')):
            pos = Positions(w, 'phrase_atom', A).get
            if all([F.ls.v(pos(1)) == 'card',
                    F.st.v(w) == 'c',
                    F.nu.v(w) == 'sg']):
                custom_quants.add(w)

        len(custom_quants)

        custom_preps = set()
        
        