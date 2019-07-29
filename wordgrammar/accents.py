import re
from positions import Positions

def book_class(word, tf):
    '''
    Returns the book accent class the 
    word belongs to as a string.
    '''
    book = tf.api.T.sectionFromNode(word)[0]
    if book not in ('Psalms', 'Job', 'Proverbs'):
        return '21'
    else:
        return '3'

def masoretic_word(word, tf):
    '''
    Returns word list of words contained in Masoretic
    concept of word; i.e. in cases where words are 
    split in BHSA but phonologically one word.
    '''
    F = tf.api.F

    mwords = [word] # collect them here
    thisword = word

    # back up `this_word` to beginning
    while '&' in str(F.trailer.v(thisword-1))\
        or F.trailer.v(thisword-1)=='':
        mwords.append(thisword-1)
        thisword = thisword-1

    # restart at middle
    thisword = word

    # move from middle to end
    while '&' in str(F.trailer.v(thisword))\
        or F.trailer.v(thisword) == '':
        mwords.append(thisword+1)
        thisword = thisword+1

    return sorted(mwords)

class Disjoint:
    
    '''
    This class analyzes and returns sets of words that
    contain a disjoint accent marker of some kind. In 
    most cases, a simple regex match is sufficient. In
    other cases, contextual information is needed. Where
    compound accents may occur, only a shallow classification 
    is attempted. In the case of potential legarmeh, for example, 
    the existence of a paseq is sufficient to conclude a disjoint 
    reading, regardless of whether the paseq and the preceding 
    accent constitute legarmeh. Another contextual case, the 
    tiphchah, depends on the accent of the subsequent word.
    '''
    
    def __init__(self, tf):
        # set up Text-Fabric classes
        self.tf = tf
        self.F, self.T, self.L = tf.api.F, tf.api.T, tf.api.L
        
    def eval_simple(self, word):
        '''
        Evaluates simple cases of disjunction
        with a regex match.
        '''
        
        # regex patterns depending on book accent class
        reg = {
            
            '21': {
                'atnach': '.*\u0591',
                'zaqeph qaton': '.*\u0594',
                'zaqeph gadol': '.*\u0595',
                'segolta': '.*\u0592',
                'shalshelet': '.*\u0593',
                'rebia': '.*\u0597',
                'zarqa': '.*\u05AE',
                'pashta': '.*\u0599',
                'yetiv': '.*\u059A', 
                'tebir': '.*\u059B',
                'geresh': '.*\u059C',
                'gershayim': '.*\u059E',
                'pazer': '.*\u05A1',
                'qarney parah': '.*\u059F',
                'telisha gedola': '.*\u05A0',
                'paseq': '.*\u05C0'
            },
            
            '3': {
                'atnach': '.*\u0591',
                'rebia': '.*\u0597',
                'oleh weyored': '.*\u05AB.*\u05A5',
                'tsinor': '.*\u0598',
                'dechi': '.*\u05AD',
                'pazer':  '.*\u05A1',
                'paseq': '.*\u05C0'
            }
        }
        
        bclass = book_class(word, self.tf)
        disaccents = '|'.join(reg[bclass].values())
        if re.match(disaccents, self.T.text(word)):
            return True
        else:
            return False
        
        
    def eval_tiphchah(self, word):
        '''
        The tiphchah accent marks disjunction
        when it is followed by a word accented
        with silluq or atnach. In the UTF8,
        silluq is not distinguished from the
        metheg. Thus we look instead for a soph pasuq.
        '''
        
        atnach_soph = '.*\u0591|.*\u05C3'

        # quick check for tiphchah accent
        if not re.match('.*\u0596', self.T.text(word)):
            return False

        P = Positions(word, 'verse', self.tf).get
        !nxt = self.T.text(P(1)) if P(1) else ' '.join(self.T.text(word).split()[1:])
        #NB THIS FUNCTION NEEDS TO BE EVALUATED MORE CLOSELY
        
        if re.match(atnach_soph, nxt):
            return True
        else:
            return False
        
        
dis21 = {
    'atnach': {'regex':'.*\u0591', 'etcbc':'92'},
    'tiphchah': {'regex':'.*\u0596', 'etcbc':'73'},
    'zaqeph qaton': {'regex':'.*\u0594', 'etcbc':'80'},
    'zaqeph gadol': {'regex':'.*\u0595', 'etcbc':'85'},
    'segolta': {'regex':'.*\u0592', 'etcbc':'01'},
    'shalshelet': {'regex':'.*\u0593', 'etcbc':'65'},
    'rebia': {'regex':'.*\u0597', 'etcbc':'81'},
    'zarqa': {'regex':'.*\u05AE', 'etcbc':'02'},
    'pashta': {'regex':'.*\u0599', 'etcbc':'03'},
    'yetiv': {'regex':'.*\u059A', 'etcbc':'10'}, 
    'tebir': {'regex':'.*\u059B', 'etcbc':'91'},
    'geresh': {'regex':'.*\u059C', 'etcbc':'61'},
    'gershayim': {'regex':'.*\u059E', 'etcbc':'62'},
    'legarmeh': {'regex':'.*\u05A3.*\u05C0', 'etcbc':'[74...05]'},
    'pazer qaton': {'regex':'.*\u05A1', 'etcbc':'83'},
    'pazer gadol': {'regex':'.*\u059F', 'etcbc':'84'},
    'telisha gedola': {'regex':'.*\u05A0', 'etcbc':'14|44'},
}
dis3 = {
    'atnach': {'regex':'.*\u0591', 'etcbc':'92'},
    'rebia': {'regex':'.*\u0597', 'etcbc':'81'},
    'oleh weyored': {'regex':'.*\u05AB.*\u05A5', 'etcbc':'.*60.*71'},
    'rebia mugrash': {'regex':'.*\u059D.*\u0597', 'etcbc':'.*11.*81'},
    'shalshelet gedolah': {'regex':'.*\u0593.*\u05C0', 'etcbc':'[65...05]'},
    'tsinor': {'regex':'.*\u0598', 'etcbc':'82'},
    'dechi': {'regex':'.*\u05AD', 'etcbc':'13'},
    'pazer': {'regex':'.*\u05A1', 'etcbc':'83'},
    'mehuppak legarmeh': {'regex':'.*\u05A4.*\u05C0', 'etcbc':'[70...05]'},
    'azla legarmeh': {'regex':'.*\u05A8.*\u05C0', 'etcbc':'[63|33...05]'}
}