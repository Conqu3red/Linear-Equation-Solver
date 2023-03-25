from typing import *
from equations import *
import mat_solver

def solve_linear(equations: List[LinearEquation], fraction_mode: bool = False) -> Optional[Dict[str, int]]:
    variables: Set[str] = set()
    for eq in equations:
        eq.isolate_const()
        print(eq)
        for var in eq.lhs.variables:
            variables.add(var)
    
    vars = list(variables)
    vars.sort()
    mat = [[eq.lhs.variables.get(var, 0) for var in vars] for eq in equations]
    target_vector = [eq.rhs.const for eq in equations]

    #print("Matrix:")
    #mat_solver.debug(mat, target_vector)

    solutions = mat_solver.mat_solve(mat, target_vector, fraction_mode=fraction_mode)
    if not solutions:
        return None

    return {var: solution for var, solution in zip(vars, solutions)}


def main():
    print("---- Linear Equation Solver v1.0.0 ----")
    print("Type in each equation followed by a newline. Press enter again to finish input.\n")
    use_fractions = input("Display result as fractions? (Y/n) ").strip().lower() != "n"
    equations = []
    i = 1
    while True:
        equation = input(f"Enter linear equation {i}: ").strip()
        if not equation:
            break
        equations.append(LinearEquation.parse(equation))
        i += 1

    # TODO: fraction mode WITH similification.
    solutions = solve_linear(equations, fraction_mode=use_fractions)
    print("Solutions:")
    if solutions:
        for var, value in solutions.items():
            print(f"    {var} = {value}")
    else:
        print(f"    No solutions.")


if __name__ == "__main__":
    main()


"""
x - y + 3z = 5
x + y + 6z = 12
3x - 2y + 2z = 10

x = 4, y = 2, z = 1


2x = 1
2x + y = 2

x + z = 5
x = y
y = 1

"""
