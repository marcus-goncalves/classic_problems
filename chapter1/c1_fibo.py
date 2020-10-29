from typing import Dict
from functools import lru_cache

# --------------- FIBO with Recusive Method ---------------
def fibo1(x: int) -> int:
    if x < 2: # Base Cases
        return x

    return fibo1(x - 2) + fibo1(x - 1) # Recursiviness

# --------------- FIBO with Recusive and Memoization ---------------
memo: Dict[int, int] = {0: 0, 1: 1} # Memoization
def fibo2(x: int) -> int:
    if x not in memo:
        memo[x] = fibo2(x -2) + fibo2(x - 1)

    return memo[x]

# --------------- FIBO with Recusive and Auto Memoization ---------------
@lru_cache(maxsize=None) # Auto Memoization
def fibo3(x: int) -> int:
    if x < 2:
        return x

    return fibo3(x - 2) + fibo3(x - 1)

# --------------- Traditional Fibo Solution ---------------
def fibo4(x: int) -> int:
    if x == 0:
        return x

    last: int = 0
    next: int = 1
    for _ in range(1, x):
        last, next = next, last + next
    
    return next

# --------------- Fibo Generator with Yeld ---------------
def fibo5(x: int) -> int:
    yield 0
    if x > 0:
        yield 1

    last: int = 0
    next: int = 1
    for _ in range(1, x):
        last, next = next, last + next
        yield next


if __name__ == "__main__":
    print(fibo1(30))
    print(fibo2(30))
    print(fibo3(30))
    print(fibo4(30))

    for _ in fibo5(50):
        print(_)