"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""
from typing import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    if len(data) < 3:
        return False

    for i in range(2, len(data)):
        if data[i] != data[i-1] + data[i-2]:
            return False
    return True


sequence1 = [0, 3, 3, 6, 9, 15, 24]
sequence2 = [1, 1, 2, 3, 5, 8, 13]
sequence3 = [0, 1, 1, 2, 4, 6, 8]

print(check_fibonacci(sequence1))
print(check_fibonacci(sequence2))
print(check_fibonacci(sequence3))