# Tynan McGee
# 4/25/2021

# add subtract mult divide, len (length of the string representation)
# repr/string, neg, pos, abs, float, round
import numpy as np

def gcd(a,b):
    if a < 0 and b < 0:
        a = -a
        b = -b
    if a < b:
        a,b = b,a
    r = a % b
    if r == 0: # remainder is 0
        return b
    return gcd(b,r)

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        if type(numerator) == float or type(numerator) == np.float64:
            self.numerator = numerator
            self.denominator = 1
            self.flt = True
        elif numerator == 0:
            self.numerator = 0
            self.denominator = 1
            self.flt = False
        else:
            div = gcd(numerator, denominator)
            self.numerator = numerator // div
            self.denominator = denominator // div
            self.flt = False
        if (self.numerator < 0 and self.denominator < 0) or (self.numerator > 0 and self.denominator < 0):
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        if self.denominator == 1:
            self.string = str(self.numerator)
        else:
            self.string = str(self.numerator) + '/' + str(self.denominator)
            
    def decimal(self):
        return self.numerator / self.denominator

    def add(self, frac):
        if self.denominator == frac.denominator:
            return Fraction(self.numerator + frac.numerator, self.denominator)
        denom = self.denominator * frac.denominator
        a_num = frac.denominator * self.numerator
        b_num = self.denominator * frac.numerator
        num = a_num + b_num
        if type(num) == float:
            return Fraction(num / denom)
        return Fraction(num, denom)
    
    def mult(self, c):
        if type(c) == int:
            num = self.numerator * c
            den = self.denominator * c
            if c < 0:
                num *= -1
        elif type(c) == float:
            num = self.decimal() * c
            return Fraction(num)
        elif isinstance(c, Fraction):
            num = self.numerator * c.numerator
            den = self.denominator * c.denominator
            if type(num) == float:
                return Fraction(num / den)
        return Fraction(num, den)
    
    def invert(self):
        if self.numerator == 0:
            return self
        return Fraction(self.denominator, self.numerator)

def get_frac_from_string(st):
    """ input is string formatted as "a/b" or "a" for integers a and b. returns fraction object with numerator a, denominator b. if input is just "a"
        returns fraction object with numeratora and denominator 1."""
    a = st.split('/')
    if len(a) == 2:
        return Fraction(int(a[0]), int(a[1]))
    elif len(a) == 1:
        if '.' in a:
            return Fraction(float(a[0]), 1)
        else:
            return Fraction(int(a[0]), 1)
    else:
        print('inputted fraction string was invalid')