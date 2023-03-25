from typing import *
from utils import *
from fraction import Fraction

def list_mult(l, scalar):
    for i in range(len(l)):
        l[i] *= scalar


def debug(mat: List[List[int]], target: List[int]):
    for i, row in enumerate(mat):
        print(f"  [{' '.join(str(x) for x in row)}] = {target[i]}")
    

def mat_solve(mat: List[List[int]], target: List[int], fraction_mode: bool = False):
    assert len(mat) == len(target) == len(mat[0])

    # goal is to make matrix like
    # a b c
    # 0 d e
    # 0 0 f

    result = [None] * len(target)

    prev_row_index = None
    while True:
        # count non-zero values in each row
        nonzero_counts = [(y, sum(v != 0 for v in row)) for y, row in enumerate(mat)]
        nonzero_counts.sort(key=lambda row: row[1])
        nonzero_counts = [c for c in nonzero_counts if c[1] > 0]
        
        # no equations left to modify, algorithm completed
        if len(nonzero_counts) == 0:
            break
        
        # select the row with the least number of significant values
        nonzero_count = nonzero_counts[0]
        row_index = nonzero_count[0]
        
        if prev_row_index == row_index:
            # unsolvable
            return None
        
        # find the first non-zero column.
        selected_row = mat[row_index]
        for var_index in range(len(selected_row)):
            if selected_row[var_index] != 0:
                break

        variable_lcm = bulk_lcm([abs(row[var_index]) for row in mat if row[var_index] != 0])
        
        # multiply all rows such that each value in the `row_index` column will be the same.
        for i, row in enumerate(mat):
            if row[var_index] != 0:
                target[i] *= variable_lcm // row[var_index]
                list_mult(row, variable_lcm // row[var_index])

        if nonzero_count[1] == 1:
            # row only has one value greater than 0, so we have a solution to result[var_index]
            if fraction_mode:
                result[var_index] = Fraction(target[var_index], selected_row[var_index])
            else:
                result[var_index] = target[var_index] / selected_row[var_index]
        
        # "substitute" into every other row to efficively zero out this column of the matrix
        for i, row in enumerate(mat):
            if i == row_index and nonzero_count[1] != 1:
                continue
            
            multiplier = 1 if row[var_index] > 0 else -1
            
            if row[var_index] != 0:
                for x in range(len(row)):
                    row[x] -= selected_row[x] * multiplier
                
                target[i] -= target[var_index] * multiplier
                row[var_index] = 0

        prev_row_index = row_index
    

    return result


if __name__ == "__main__":
    solutions = mat_solve(
        [
            [1, -1, 3],
            [1, 1, 12],
            [3, 0, 2],
        ],
        [5, 12, 10]
    )

    solutions = mat_solve(
        [
            [1, -1, 3],
            [0, 0, 12],
            [3, 0, 2],
        ],
        [5, 12, 10]
    )

    solutions = mat_solve(
        [
            [1, -1, 3],
            [1, 1, 6],
            [3, -2, 2],
        ],
        [5, 12, 10]
    )

    print(solutions)