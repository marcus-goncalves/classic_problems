from __future__ import annotations
from dataclasses import dataclass
from edge import Edge


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.vertex_to, self.vertex_from, self.weight)
    
    def __lt__(self, other: WeightedEdge) -> bool:
        return self.weight < other.weight
    
    def __str__(self) -> str:
        return f'{self.vertex_from} {self.weight} > {self.vertex_to}'