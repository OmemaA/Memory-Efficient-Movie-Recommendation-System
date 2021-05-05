import math
import bitarray
import mmh3

class bloomFilter():
    def __init__(self, total, bits=None, hashes=None,**kwargs ):        
        #calculates false positive probability
        # self.fp = self.get_fp()
        self.fp = 0.001

        #calculates the size of bit array
        self.bits = self.get_size(total, self.fp)

        #calculates optimum numb of hash function to use
        self.totalhash = self.get_total_hash(self.bits, total)

        # setting values for bits and hashes, if given
        if bits !=0: self.bits = bits
        if hashes !=0: self.totalhash = hashes
        
        #creates a bit array of the given size
        self.bitarray = bitarray.bitarray(self.bits)
        #initializes all bits to 0
        self.bitarray.setall(0)

        if len(kwargs)>0:
            a=bitarray.bitarray(endian="big")
            self.bitarray= a.frombytes(kwargs["bits1"])        
            self.bitarray=a
        else:
            #creates a bit array of the given size
            self.bitarray = bitarray.bitarray(self.bits)
            #initializes all bits to 0
            self.bitarray.setall(0)

        #total items added
        self.items = 0

    
    def get_fp(self):
        return (1- math.exp(-(self.totalhash * self.items) / self.bits)) ** self.totalhash

    def add(self, element):
        for i in self.element_index(element):
            self.bitarray[i] = 1
        self.items += 1 

    def check(self, element):
        for i in self.element_index(element):
            if self.bitarray[i] == 0:
                return False
        return True

    def get_size(self, total, fp):
        m = -(total* math.log(fp))/(math.log(2)**2)
        return round(m) 

    def get_total_hash(self, bits, total):
        k = (bits/total) * math.log(2)
        return round(k)        

    def hash_index(self, hash):
        return hash % self.bits
    
    def element_index(self, element):
        return [self.hash_index(mmh3.hash(element, i))for i in range(self.totalhash)]
    
    def similarity_value(self,other):
        andarray= (self.bitarray & other.bitarray)
        return 2*(andarray.count())/(self.bitarray.count(1) + other.bitarray.count(1))
#         andarray= (self.bitarray & other.bitarray)
#         xnorarray = (~self.bitarray & ~other.bitarray)
#         x=(self.bitarray | other.bitarray).count()
#         totalpossibleval= x *coefficient + (1-coefficient) * (self.bits-x) 
#         # totalpossibleval = totalpossibleval.count()
#         if totalpossibleval==0:
#             return 0
#         andval=andarray.count()
#         xnorval=xnorarray.count()
#         return (coefficient*andval + (1-coefficient)*xnorval)/totalpossibleval
