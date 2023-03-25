from typing import *
from equations import *

def compute_gcd(x: int, y: int):
    while y:
        x, y = y, x % y
    return x


def compute_lcm(x: int, y: int):
   return (x * y) // compute_gcd(x, y)


def bulk_lcm(nums: List[int]):
    lcm = 1
    for num in nums:
        lcm = compute_lcm(lcm, num)
    
    return lcm



def substitute(eq: LinearEquation, variable: str, value: EquationSide):
    """ Assumes that n * variable is in eq and that n * variable """
    for k, v in value.variables.items():
        eq.lhs.variables[k] = eq.lhs.variables.get(k, 0) + v
    
    eq.lhs.variables[variable] = 0
    eq.lhs.clean()
    eq.rhs.const -= value.const
    

def solve_linear(equations: List[LinearEquation]):
    variables: Set[str] = set()
    for eq in equations:
        eq.isolate_const()
        for var in eq.lhs.variables:
            variables.add(var)
    
    if len(equations) == 1:
        if len(variables) == 1:
            v = variables.pop()
            eq = equations[0]
            return {v: eq.rhs.const / eq.lhs.variables[v]}
        else:
            raise Exception(f"Cannot solve, {equations}")
    
    #for eq in equations:
    #    for var in variables:
    #        eq.lhs.variables[var] = eq.lhs.variables.get(var, 0)

    for var in sorted(list(variables)):
        v_coeffs = [abs(eq.lhs.variables[var]) for eq in equations if eq.lhs.variables.get(var)]
        lcm = bulk_lcm(v_coeffs)
        print(var, lcm)

        for eq in equations:
            if eq.lhs.variables.get(var, 0) != 0:
                print(lcm // eq.lhs.variables[var])
                eq.multiply(lcm // eq.lhs.variables[var])
                eq.lhs.clean()
            else:
                print("zero", eq)
        
        for eq in equations:
            print("   ", eq)

        rearrange = equations[0]
        #for eq in equations:
        #    if len(eq.lhs.variables) < len(rearrange.lhs.variables):
        #        rearrange = eq
        
        print("TO REARRANGE:", rearrange)
        rearrange = deepcopy(rearrange)
        # rearrange
        for k, val in rearrange.lhs.variables.items():
            if k == var: continue
            rearrange.lhs.variables[k] = 0
            rearrange.rhs.variables[k] = -val
        
        rearrange.lhs.clean()
        print("REARRANGED:", rearrange)

        for eq in equations[1:]:
            substitute(eq, var, rearrange.rhs)
        
        for eq in equations[1:]:
            print("   ", eq)
        
        values = solve_linear(equations[1:])

        # solve for actual value of var
        # TODO
        eq = equations[0]
        for k, v in values.items():
            if eq.lhs.variables.get(k, 0) != 0:
                substitute(eq, k, EquationSide({}, v * eq.lhs.variables[k]))
        
        print("s", eq)
        return {**values, var: eq.rhs.const / eq.lhs.variables[var]}
        break
        
""" 

equations = [
    LinearEquation.parse("x - y + 3z = 5"),
    LinearEquation.parse("x + y + 6z = 12"),
    LinearEquation.parse("3x - 2y + 2z = 10"),
]

solutions = solve_linear(equations)

for var, value in solutions.items():
    print(var, "=", value)
print()
for eq in equations:
    print(eq) """