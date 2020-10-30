from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List
from typing import Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop

T = TypeVar('T')
C = TypeVar('C', bound='Comparable')

def linear_search(iterable: Iterable[T], search_term: T) -> bool:
    for item in iterable:
        if item == search_term:
            return True
    return False

def binary_search(sequence: Sequence[C], search_term: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1

    while low <= high:
        mid: int = (low + high) // 2

        if sequence[mid] < search_term:
            low = mid + 1
        elif sequence[mid] > search_term:
            high = mid - 1
        else:
            return True
    return False

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...
    
    def __lt__(self, other: C) -> bool:
        ...
    
    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other
    
    def __le__(self: C, other: C) -> bool:
        # return self < other or self == other
        return self <= other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


if __name__ == "__main__":
    print(linear_search([1, 5, 15, 15, 15, 15, 20], 5))
    print(binary_search(['a', 'b', 'c', 'g', 'k', 'z'], 'g'))
    print(binary_search(['john', 'mark', 'ronald', 'sarah'], 'Luca'))