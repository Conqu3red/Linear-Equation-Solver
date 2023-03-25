from typing import *
from utils import *

class Fraction:
    def __init__(self, numerator: int, denominator: int) -> None:
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()
    
    def simplify(self):
        gcd = compute_gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // gcd
        self.denominator = self.denominator // gcd
    
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)

        return f"{self.numerator} / {self.denominator}"