from typing import *
from dataclasses import dataclass
import string
from copy import deepcopy

class Term(NamedTuple):
    coefficient: int
    variable: Optional[str]

    @classmethod
    def parse(cls, term: str):
        variable = None
        if term[-1] in string.ascii_letters:
            coeff_string = term[:-1]
            if not coeff_string or coeff_string == "+":
                coefficient = 1
            elif coeff_string == "-":
                coefficient = -1
            else:
                coefficient = int(coeff_string)
            variable = term[-1]
        else:
            coefficient = int(term)
        
        return cls(coefficient, variable)
    
@dataclass
class EquationSide:
    variables: Dict[str, int]
    const: int

    @classmethod
    def parse(cls, side: str):
        variables = {}
        const = 0
        side = side.strip()
        buf = ""
        
        def process_buf():
            nonlocal variables, const
            term = Term.parse(buf)
            if term.variable is None:
                const += term.coefficient
            else:
                variables[term.variable] = variables.get(term.variable, 0) + term.coefficient
            
        i = 0
        while i < len(side):
            token = side[i]
            if not token.isspace():
                is_end_of_var = buf and buf[-1] in string.ascii_letters
                is_end_of_const = buf and buf[-1].isnumeric() and not token.isalnum()
                
                if is_end_of_var or is_end_of_const:
                    process_buf()
                    buf = ""
            
                buf += token
            
            i += 1
        
        if buf:
            process_buf()
        
        return cls(variables, const)

    def clean(self):
        self.variables = {k: v for k, v in self.variables.items() if v != 0}

    def multiply(self, amount: int):
        for k in self.variables:
            self.variables[k] *= amount
        
        self.const *= amount
    
    def add(self, other: 'EquationSide'):
        for k, v in other.variables.items():
            self.variables[k] = self.variables.get(k, 0) + v
        
        self.const += other.const
    
    def subtract(self, other: 'EquationSide'):
        for k, v in other.variables.items():
            self.variables[k] = self.variables.get(k, 0) - v
        
        self.const -= other.const
    
    def __str__(self):
        pairs = list(self.variables.items())
        pairs.sort(key=lambda x: x[0])
        result = []
        for k, v in pairs:
            if v == 0: continue
            
            if result and v > 0: result.append("+")
            if v < 0: result.append("-")
            
            if v != 1:
                result.append(str(abs(v)) + k)
            else:
                result.append(k)
        
        if self.const != 0 or not result:
            if result and self.const > 0: result.append("+")
            if self.const < 0: result.append("-")
            result.append(str(abs(self.const)))
    
        return " ".join(result)


@dataclass
class LinearEquation:
    lhs: EquationSide
    rhs: EquationSide

    @classmethod
    def parse(cls, equation: str):
        lhs, rhs = equation.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()

        lhs_parsed = EquationSide.parse(lhs)
        rhs_parsed = EquationSide.parse(rhs)

        return cls(lhs_parsed, rhs_parsed)

    def isolate_const(self):
        if self.lhs.const > self.rhs.const:
            self.rhs, self.lhs = self.lhs, self.rhs
        
        self.rhs.const -= self.lhs.const
        self.lhs.const = 0

        for k, v in self.rhs.variables.items():
            self.lhs.variables[k] = self.lhs.variables.get(k, 0) - v
        
        self.rhs.variables.clear()
    
    def multiply(self, amount: int):
        self.lhs.multiply(amount)
        self.rhs.multiply(amount)
    
    def __str__(self):
        return f"{self.lhs!s} = {self.rhs!s}"