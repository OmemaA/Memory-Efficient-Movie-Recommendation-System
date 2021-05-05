import math
import bitarray
import mmh3

class bloomFilter():
    def __init__(self, total):        
        #calculates false positive probability
        self.fp = self.get_fp()

        #calculates the size of bit array
        self.bits = self.get_size(total, self.fp)

        #calculates optimum numb of hash function to use
        self.totalhash = self.get_total_hash(self.bits, total)

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
        return int(m) 

    def get_total_hash(self, bits, total):
        k = (bits/total) * math.log(2)
        return int(k)        

    def hash_index(self, hash):
        return hash % self.bits
    
    def element_index(self, element):
        return [self.hash_index(mmh3.hash(i, element))for i in range(self.totalhash)]

# obj = bloomFilter(1000)
# obj.add("Hello")
# obj.add("Hi")
# obj.add("Hand")
# obj.add("Yallow")
# obj.check("Yellow")


