from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    vertex_from: int # Known as u
    vertex_to: int # Known as v

    def reversed(self) -> Edge:
        return Edge(self.vertex_to, self.vertex_from)

    def __str__(self) -> str:
        return f'{self.vertex_from} -> {self.vertex_to}'
