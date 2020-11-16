from __future__ import annotations
import sys
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass
from mst import WeightedPath, print_weighted_path
from weighted_edge import WeightedEdge
from weighted_graph import WeightedGraph
sys.path.append([0, '..'])
from chapter2.c2_generic_search import PriorityQueue


V = TypeVar('V')

@dataclass
class DijkstraNode:
    vertex: int
    distance: float
    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance
    
    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance

def dijsktra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)
    distances: List[Optional[float]] = [None] * wg.vertex_count
    path_dict: Dict[int, WeightedEdge] = {}
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    
    distances[first] = 0
    pq.push(DijkstraNode(first, 0))

    while not pq.empty:
        vertex_from: int = pq.pop().vertex
        dist_vertex_from: float = distances[vertex_from]

        for we in wg.edges_for_index(vertex_from):
            dist_vertex_to: float = distances[we.vertex_to]

            if dist_vertex_to is None or dist_vertex_to > we.weight + dist_vertex_from:
                distances[we.vertex_to] = we.weight + dist_vertex_from
                path_dict[we.vertex_to] = we
                pq.push(DijkstraNode(we.vertex_to, we.weight + dist_vertex_from))
    return distances, path_dict

def distance_array_to_vertex_dict(wg: WeightedGraph[V],
                                  distances: List[Optional[float]]) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict

def path_dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []
    
    edge_path: WeightedPath = []
    e: WeightedEdge = path_dict[end]
    edge_path.append(e)

    while e.vertex_from != start:
        e = path_dict[e.vertex_from]
        edge_path.append(e)
    return list(reversed(edge_path))

if __name__ == "__main__":
    city_graph2: WeightedGraph[str] = WeightedGraph(['Seattle', 'San Francisco', 'Los Angeles',
        'Riverside', 'Phoenix', 'Chicago', 'Boston', 'New York', 'Atlanta', 'Miami',
        'Dallas', 'Houston', 'Detroit', 'Philadelphia', 'Washington'])
    
    city_graph2.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_graph2.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph2.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_graph2.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph2.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_graph2.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph2.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_graph2.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_graph2.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_graph2.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_graph2.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_graph2.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_graph2.add_edge_by_vertices("Dallas", "Houston", 225)
    city_graph2.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_graph2.add_edge_by_vertices("Houston", "Miami", 968)
    city_graph2.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_graph2.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_graph2.add_edge_by_vertices("Atlanta", "Miami", 604)
    city_graph2.add_edge_by_vertices("Miami", "Washington", 923)
    city_graph2.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_graph2.add_edge_by_vertices("Detroit", "Boston", 613)
    city_graph2.add_edge_by_vertices("Detroit", "Washington", 396)
    city_graph2.add_edge_by_vertices("Detroit", "New York", 482)
    city_graph2.add_edge_by_vertices("Boston", "New York", 190)
    city_graph2.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_graph2.add_edge_by_vertices("Philadelphia", "Washington", 123)

    distances, path_dict = dijsktra(city_graph2, 'Los Angeles')
    name_distance: Dict[str, Optional[int]] = \
        distance_array_to_vertex_dict(city_graph2, distances)
    
    print('Distances from Los Angeles')
    for key, value in name_distance.items():
        print(f'{key}: {value}')
    print('')
    print('Shotest path:')
    path: WeightedPath = path_dict_to_path(city_graph2.index_of('Los Angeles'), 
                                           city_graph2.index_of('Boston'),
                                           path_dict)
    print_weighted_path(city_graph2, path)