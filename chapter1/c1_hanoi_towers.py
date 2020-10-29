"""
Hanoi Towers:
- 3 Columns: A == B == C
- 3 Discs from different sizes: 1 > 2 > 3
Rules:
- Only 1 Disc can be move at time
- Only the first Disc can be moved
- A bigger Disc cannot be over a smaller Disc
Solution:
- Put the 3 Discs on the third Tower
"""
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        self._container.pop()
    
    def __repr__(self) -> str:
        return repr(self._container)

def move_discs(begin: Stack[int], end: Stack[int], tmp: Stack[int], n: int) -> None:
    print(n)
    if n == 1:
        end.push(begin.pop())
    else:
        move_discs(begin, tmp, end, n - 1)
        move_discs(begin, end, tmp, 1)
        move_discs(tmp, end, begin, n - 1)
    print(tower_a, tower_b, tower_c)

if __name__ == "__main__":
    num_discs: int = 3
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()

    for i in range(1, num_discs + 1):
        tower_a.push(i)
    
    print(tower_a, tower_b, tower_c)

    move_discs(tower_a, tower_c, tower_b, num_discs)

    
