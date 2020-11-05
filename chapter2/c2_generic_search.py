from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List
from typing import Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop

T = TypeVar('T')
C = TypeVar('C', bound='Comparable')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
    
    def __repr__(self) -> str:
        return repr(self._container)
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        return self._container.pop()


class Node(Generic[T]):
    def __init__(self,
                 state: T,
                 parent: Optional[Node],
                 cost: float = 0.0,
                 heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic
    
    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


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


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()
    
    def __repr__(self) -> str:
        return repr(self._container)
    
    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> T:
        return self._container.append(item)
    
    def pop(self) -> T:
        return self._container.popleft()


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def __repr__(self) -> str:
        return repr(self._container)

    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item: T) -> None:
        heappush(self._container, item)
    
    def pop(self) -> T:
        return heappop(self._container)


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

def dfs(initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    
    # Places that are not visited by the algorithm
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    # Places that are already visited
    explored: Set[T] = {initial}

    # Seach loop
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # Success
        if goal_test(current_state):
            return current_node
        
        # Where to go next
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None

def bfs(initial: T,
        goal_test: Callable[[T], bool],
        successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))

    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node
        
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    
    return None

def astar(initial: T,
          goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))

    explored: Dict[T, float] = {initial: 0.0}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node
        
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
            
    return None



def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]

    # Inverted path
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()

    return path



if __name__ == "__main__":
    print(linear_search([1, 5, 15, 15, 15, 15, 20], 5))
    print(binary_search(['a', 'b', 'c', 'g', 'k', 'z'], 'g'))
    print(binary_search(['john', 'mark', 'ronald', 'sarah'], 'Luca'))