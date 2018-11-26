"""
Submission by:
Thien Nguyen (tn518 / 01565994)
Jinwei Zhang (jz2618 / 01540854)
"""

class Gates:
    
    def NOT(self, tup):
        try:
            x = tup[0]
        except:
            x = tup
        if x is 1:
            return 0
        return 1
       
    def OR(self, tup):
        x, y = tup
        if x == y and x == 0:
            return 0
        return 1
    
    def AND(self, tup):
        x, y = tup
        if x == y and x == 1:
            return 1
        return 0
    
    def XOR(self, tup):
        x, y = tup
        if x == y:
            return 0
        return 1
    
    def NOR(self, tup):
        return self.NOT(self.OR(tup))
    
    def NAND(self, tup):
        return self.NOT(self.AND(tup))
   
    def XNOR(self, tup):
        return self.NOT(self.XOR(tup))
    
    def ADD(self,tup):
        x,y = tup
        if x is 0:
            if y is 1:
                return 1
            else:
                return 0
        else:
            if y is 1:
                return 1
            else:
                return 0
