from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod


# FLOW
# 1. Create an Initial random Population 
# 2. Check the fitness levels: If any exceedes the threshold, terminate.
# 3. Select random individuals to reproduce themselves, with higher probabilities
# for the highest fitness levels
# 4. Do an crossover
# 5. Do a mutation with a low probability
# 6. Go back to step2
# Creation >> Evaluation >> Selection >> Crossover >> Mutation


T = TypeVar('T', bound='Chromosome')

class Chromosome:
    @abstractmethod
    def fitness(self) -> float:
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...
    
    @abstractmethod
    def mutate(self) -> None:
        ...

