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
        except:
            return self.default
        
    def index(self, i):
        try:
            return self.iterable.index(i)
        except:
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
        self.thisotype = tf.api.F.otype.v(n) if n else ''
        self.context = self.get_context(context) if n else 0
    
    def get(self, position, features=None):
        '''
        Get a node (+/-)N positions away, 
        with an option to get values for specified features.
        '''
        
        if not self.n:
            return None
        
        L, Fs = self.tf.L, self.tf.Fs # TF classes
        positions = set(L.d(self.context, self.thisotype))
        
        if position < 0:
            method = L.p
        else:
            method = L.n
            
        get_pos = self.n
        for count in range(0, abs(position)):
            get_pos = next(iter(method(get_pos, self.thisotype)), 0)
        
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

class Walker:    
    """Prepares paths from a source TF node to a target node.
    
    Supplies methods to walk forward or backward in a context until 
    encountering a TF node that meets a set of conds.
    
    Methods:
        ahead: Walk ahead from start node to target.
        back: Walk back from start node to target.
        firstresult: Return the first node in a path that
            returns True for a supplied function
    """
    
    def __init__(self, n, context, tf=None):
        """Initialize paths for a node.
        Arguments:
            n: Text-Fabric corpus node
            context: otype string of the supplied node's context to lookup
            tf: Running instance of Text-Fabric corpus
        """
        tf = tf.api
        thisotype = tf.F.otype.v(n) if n else ''
        context = tf.L.u(n, context)[0]
        self.positions = list(tf.L.d(context, thisotype))
        self.index = self.positions.index(n)
        
    def ahead(self, val_funct, stop=None, go=None):
        """Walk ahead to node.
        
        Args:
            val_funct: a function that accepts a node argument
                and returns Boolean. This determines which word
                to return.
            stop: a function that accepts a node argument and
                returns Boolean. Determines whether to interrupt 
                the walk and return None.
            go: opposite of stop, a function that accepts a node
                argument and returns Boolean. Determines whether
                to keep going in a walk.
            
        Returns:
            integer which corresponds to a Text-Fabric node
        """
        path = self.positions[self.index+1:]
        stop = stop or (lambda n: False)
        go = go or (lambda n: True)
        return self.firstresult(path, val_funct, stop, go)
            
    def back(self, val_funct, stop=None, go=None):
        """Walk back to node.
        
        Args:
            val_funct: a function that accepts a TF node argument
                and returns Boolean. Determines which word to return
                in the walk.
            stop: a function that accepts a TF node argument and
                returns Boolean. Determines whether to interrupt 
                the walk and return None.
            go: opposite of stop, a function that accepts a node
                argument and returns Boolean. Determines whether
                to keep going in a walk.
                
        Returns:
            integer which corresponds to a Text-Fabric node
        """
        path = self.positions[:self.index]
        path.reverse()
        stop = stop or (lambda n: False)
        go = go or (lambda n: True)
        return self.firstresult(path, val_funct, stop, go)
        
    def firstresult(self, path, val_funct, stop, go):
        """Return first node in a loop where val_funct(node) == True."""
        for node in path:
            # do matches
            if val_funct(node):
                return node
            # do interrupts on go
            elif not go(node):
                break
            # do interrupts on stop
            elif stop(node):
                break
   