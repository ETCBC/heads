'''
The Getter class provides list-like interactions
with safe-indexing for indices lying beyond the list's limits.
The Positions class delivers positional
data on demand when instanced on a TF node.
'''

class Getter:
    '''
    A class to safely index beyond the limits of
    an iterable with a default returned.
    Like dict.get but for iterables.
    '''
    
    def __init__(self, iterable, default=None):
        self.iterable = iterable
        self.default = default
        
    def __iter__(self):
        for i in self.iterable:
            yield i
        
    def __getitem__(self, key):
        try:
            return self.iterable[key]
        except IndexError:
            return self.default
        
    def index(self, i):
        try:
            return self.iterable.index(i)
        except ValueError:
            return self.default

class Positions:
    '''
    For a given node, provides access to nodes
    that are (+/-)N positions away in terms of 
    node adjacency within a given context.
    The context must be a nodeType that is larger
    than the supplied node.
    '''
    
    def __init__(self, n, context, tf=None):
        self.tf = tf.api # make TF classes avail
        self.n = n
        self.thisotype = tf.api.F.otype.v(n)
        self.context = self.get_context(context)
    
    def get(self, position, features=None):
        '''
        Get a node (+/-)N positions away, 
        with an option to get values for specified features.
        '''
        L, Fs = self.tf.L, self.tf.Fs # TF classes
        positions = set(L.d(self.context, self.thisotype))
        
        if position < 0:
            method = L.p
        else:
            method = L.n
            
        get_pos = self.n
        for count in range(0, abs(position)):
            get_pos = Getter(method(get_pos, self.thisotype))[0]
        
        # return None, empty string, or empty set if beyond boundaries
        if get_pos not in positions:
            if not features:
                return None
            elif len(features.split())==1:
                return ''
            else:
                return set()
        
        # simple node return
        if not features:
            return get_pos
        
        # give single feature
        if len(features.split())==1:
            return Fs(features).v(get_pos)
        
        # give pl features
        elif features:
            feats = set()
            for f in features.split():
                feats.add(Fs(f).v(get_pos))
            return feats
    
    def get_context(self, otype):
        '''
        Returns a requested context node.
        '''
        otypeRank = self.tf.otypeRank # TF classes
        L = self.tf.L
        
        if otypeRank[self.thisotype] > otypeRank[otype]:
            raise Exception('Provided context is smaller than the provided node!')
        else:
            return Getter(L.u(self.n, otype))[0]