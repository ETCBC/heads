
class Accents:
    
    def __init__(self, tf):
    
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

# prepare book 2 conjunction regex mapping
dis21_re = '|'.join(d['regex'] for n, d in dis21.items())
dis3_re = '|'.join(d['regex'] for n, d in dis3.items())
book2dis = {}
for b in F.otype.s('book'):
    if F.book.v(b) in ('Psalmi', 'Job', 'Proverbia'):
        book2dis[b] = dis3_re
    else:
        book2dis[b] = dis21_re