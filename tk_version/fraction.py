# Tynan McGee
# 5/10/2021

import numpy as np

def gcd(a,b):
    """
    Returns the greates common divisor of a and b.
    - a and b are integers.
    - Returns an integer.
    """
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
        # numerator is a nonzero integer, denominator is a nonzero integer
        if type(numerator) == int and numerator != 0 and type(denominator) == int and denominator != 0:
            div = gcd(numerator, denominator)
            self.numerator = numerator // div
            self.denominator = denominator // div
            self.flt = False
        # if numerator or denominator is a float, don't bother with the gcd and just do num/1
        elif isinstance(numerator, (float, np.floating)) or isinstance(denominator, (float, np.floating)):
            self.numerator = numerator / denominator
            self.denominator = 1
            self.flt = True
        # if numerator is 0, do 0/1
        elif numerator == 0:
            self.numerator = 0
            self.denominator = 1
            self.flt = False
        elif denominator == 0:
            raise ZeroDivisionError('You had a fraction with denominator 0.')

        # change -1/-2 --> 1/2,   change 1/-2 --> -1/2
        if (self.numerator < 0 and self.denominator < 0) or (self.numerator > 0 and self.denominator < 0):
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.numerator) + '/' + str(self.denominator)

    def __add__(self, n):
        if isinstance(n, Fraction):
            if self.denominator == n.denominator:
                return Fraction(self.numerator + n.numerator, self.denominator)
            denom = self.denominator * n.denominator
            a_num = n.denominator * self.numerator
            b_num = self.denominator * n.numerator
            num = a_num + b_num
            if type(num) == float:
                return Fraction(num / denom)
            return Fraction(num, denom)
        if isinstance(n, (int, float, np.floating, np.integer)):
            return self + Fraction(n)
        return NotImplemented

    def __radd__(self, n):
        return self + n

    def __sub__(self, n):
        if isinstance(n, (Fraction, int, float, np.floating, np.integer)):
            return self + -n
        return NotImplemented

    def __rsub__(self, n):
        return -self + n

    def __mul__(self, n):
        if isinstance(n, (int, np.integer)):
            num = self.numerator * n
            den = self.denominator
        elif isinstance(n, (float, np.floating)):
            num = self.decimal() * n
            den = 1
        elif isinstance(n, Fraction):
            num = self.numerator * n.numerator
            den = self.denominator * n.denominator
        else:
            return NotImplemented
        return Fraction(num, den)

    def __rmul__(self, n):
        return self * n

    def __truediv__(self, n):
        if isinstance(n, Fraction):
            return self * n.invert()
        if isinstance(n, (int, float, np.floating, np.integer)):
            return self * Fraction(1, n)
        return NotImplemented

    def __rtruediv__(self, n):
        return self.invert() * n

    def __neg__(self):
        return self * -1
    
    def __abs__(self):
        if self.numerator < 0:
            return self * -1
        return self

    ### COMPARISON OPERATORS ###
    # to avoid dividing, we multiply over on the fractions when comparing
    # for example, instead of a/b < c/d, we do ad < cb
    # instead of a/b < n, we do a < nb
    # denominators are nonnegative because of the way fraction objects
    # are constructed, so the inequality sign never switches when we multiply over
    def __lt__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator < n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator < self.denominator * n
        return NotImplemented

    def __le__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator <= n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator <= self.denominator * n
        return NotImplemented

    def __gt__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator > n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator > self.denominator * n
        return NotImplemented

    def __ge__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator >= n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator >= self.denominator * n
        return NotImplemented

    def __eq__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator == n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator == self.denominator * n
        # elif isinstance(n, str):
        #     return n == str(self)
        return False # if n isn't a number or fraction, then it's not equal

    def __ne__(self, n):
        if isinstance(n, Fraction):
            return self.numerator * n.denominator != n.numerator * self.denominator
        if isinstance(n, (int, float, np.integer, np.floating)):
            return self.numerator != self.denominator * n
        # elif isinstance(n, str):
        #     return n != str(self)
        return True # if n isn't a number or fraction, then it's not equal


    def __len__(self):
        # we define len of a fraction object to be the length of its string representation
        return len(str(self))

    def invert(self):
        if self.numerator == 0:
            return self
        return Fraction(self.denominator, self.numerator)

    def __float__(self):
        return self.numerator / self.denominator
    def decimal(self):
        return self.numerator / self.denominator


def get_frac_from_string(st):
    """
    Takes in a string ("a/b") and returns a fraction object.
    If there is no denominator in the string, returns "a/1".
    - st is a string which looks like a fraction "a/b" 
      where a and b are integers.
    - Returns fraction object representing 
      the number in the string (numerator a, denominator b).
    """
    a = st.split('/')
    if len(a) == 2:
        return Fraction(int(a[0]), int(a[1]))
    if len(a) == 1: # a is either int or float
        if '.' in a[0]:
            return Fraction(float(a[0]), 1)
        return Fraction(int(a[0]), 1)
    print('inputted fraction string was invalid')
    return None

def get_decimal_from_float(n):
    """
    Retrieves the decimal portion from floating number n using its string.
    Example: turns n = 1.2345 --> n = 0.2345.
    Use of string is for zero loss of accurracy.
    - n is a float.
    - Returns a float.
    """
    n = str(n).split('.')
    # n looks like ['3', '2345']
    n = '0.' + n[1]
    return float(n)

def dec_to_frac_approx(n, accuracy=0.00001):
    """
    Converts floating number n to a fraction object 
    approximation using the Stern-Brocot Tree.
    - n is a float.
    - accuracy is a float determining how accurate the result should be.
    - Returns a fraction object.
    """
    # get the decimal part of n
    if isinstance(n, Fraction):
        if not n.flt:
            return n
        else:
            n = float(n)
    if not n or n < 0.0000000001: # n is 0 (or sufficiently close to 0)
        return Fraction()
    sign = 1
    if n < 0:
        n = -n
        sign = -1
    error = n * accuracy
    a = int(np.floor(n))
    n = get_decimal_from_float(n)
    if not n: # decimal part is 0
        return Fraction(a)
    lower_n = 0
    lower_d = 1
    upper_n = 1
    upper_d = 1
    # start with 0/1 < n < 1/1
    # take mediant of the lower and upper bounds to get a new fraction
    # that's within the old range
    while True:
        middle_n = lower_n + upper_n
        middle_d = lower_d + upper_d
        if middle_d * (n + error) < middle_n:
            # x < middle_n / middle_d, so use that as the new
            # upper bound
            upper_n = middle_n
            upper_d = middle_d
        elif middle_n < middle_d * (n - error):
            # x > middle_n / middle_d, so use that as the new
            # lower bound
            lower_n = middle_n
            lower_d = middle_d
        else:
            # middle_n / middle_d is within |error| of x
            middle_n *= sign
            a *= sign
            return Fraction(middle_n, middle_d) + a

def dec_to_frac_exact(n):
    """
    Converts floating point number n to a fraction object with 100% accuracy by
    multiplying the decimal by 10^n where n is # of decimal places and then dividing
    by 10^n.
    - n is a float.
    - Returns a fraction object.
    """
    if isinstance(n, Fraction):
        if not n.flt:
            return n
        else:
            n = float(n)
    sign = 1
    if n < 0:
        n = -n
        sign = -1
    a = int(np.floor(n))
    n = get_decimal_from_float(n)
    dec_num = len(str(n)) - 2 # removes the '0.' at the start
    power = 10 ** dec_num
    n *= power
    n = int(n)

    n *= sign
    a *= sign
    return Fraction(n, power) + a



if __name__ == "__main__":
    print(get_decimal_from_float(1.234567))