from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint


Point = TypeVar('Point', bound=DataPoint)

def zscores(original:Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)

    if std == 0:
        return [0] * len(original)
    
    return [(x - avg) / std for x in original]

class Kmeans(Generic[Point]):
    def __init__(self, k: int, points: List[Point]) -> None:
        if k < 1:
            raise ValueError('K must be >= 1')
        
        self._points: List[Point] = points
        self._zscore_normalize()
        self._clusters: List[Kmeans.Cluster] = []

        for _ in range(k):
            rand_point: DataPoint = self._random_point()
            cluster: Kmeans.Cluster = Kmeans.Cluster([], rand_point)
            self._clusters.append(cluster)

    @dataclass
    class Cluster():
        points: List[Point]
        centroid: DataPoint
    
    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]
    
    def _dimesion_slice(self, dimension: int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]

    def _zscore_normalize(self) -> None:
        zscored: List[List[float]] = [[] for _ in range(len(self._points))]

        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimesion_slice(dimension)
            for idx, zscore in enumerate(zscores(dimension_slice)):
                zscored[idx].append(zscore)
        
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])

    def _random_point(self) -> DataPoint:
        rand_dimensions: List[float] = []

        for dimension in range(self._points[0].num_dimensions):
            values: List[float] = self._dimesion_slice(dimension)
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
        return DataPoint(rand_dimensions)
    
    def _assign_clusters(self) -> None:
        for point in self._points:
            closest: DataPoint = min(
                self._centroids,
                key=partial(DataPoint.distance,
                point))
            idx: int = self._centroids.index(closest)
            cluster: Kmeans.Cluster = self._clusters[idx]
            cluster.points.append(point)

    def _generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) == 0:
                continue
            
            means: List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [p.dimensions[dimension] for p in cluster.points]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)
    
    def run(self, max_iterations: int = 100) -> List[Kmeans.Cluster]:
        for iteration in range(max_iterations):
            for cluster in self._clusters:
                cluster.points.clear()
        
            self._assign_clusters()
            old_centroids: List[DataPoint] = deepcopy(self._centroids)
            self._generate_centroids()

            if old_centroids == self._centroids:
                print(f'Converged afer {iteration} epochs.')
                return self._clusters
        return self._clusters

if __name__ == "__main__":
    p1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    p2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    p3: DataPoint = DataPoint([3.0, 1.5, 2.5])
    kmeans_test: Kmeans[DataPoint] = Kmeans(2, [p1, p2, p3])
    test_clusters: List[Kmeans.Cluster] = kmeans_test.run()

    for idx, cluster in enumerate(test_clusters):
        print(f'Cluster {idx}: {cluster.points} ')