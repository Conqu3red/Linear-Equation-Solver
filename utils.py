from typing import *

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