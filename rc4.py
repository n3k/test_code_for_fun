class RC4(object):
    
    def __init__(self, seed):
        self.seed = seed
        self.S = range(256)
        self.K = []
        for i in xrange(0, 256):
            self.K.append(ord(self.seed[i % len(self.seed)]))
        self.ksa()
        
    
    def _swap(self, i, j):
        aux = self.S[i]
        self.S[i] = self.S[j]
        self.S[j] = aux

    def ksa(self):
        j = 0
        for i in xrange(0,255):
            j = (j + self.S[i] + self.K[i]) & 255
            self._swap(i, j)
            
    def prga(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) & 255
            j = (j + self.S[i]) & 255
            self._swap(i, j)
            t = (self.S[i] + self.S[j]) & 255
            yield self.S[t]

a = RC4("ABCDEFGH")
b = a.prga()
text = "Hello World and GoodBye"
for x in text:
    print hex(ord(x) ^ b.next())