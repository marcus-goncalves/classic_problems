import csv
from typing import List, Tuple
from util import feature_scaling
from network import Network
from random import shuffle


def interpret(output: List[float]) -> int:
    if max(output) == output[0]:
        return 1
    elif max(output) == output[1]:
        return 2
    else:
        return 3

if __name__ == "__main__":
    wine_params: List[List[float]] = []
    wine_class: List[List[float]] = []
    wine_species: List[int] = []

    with open('wine.data', mode='r') as file:
        wines: List = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
        shuffle(wines)

        for wine in wines:
            params: List[float] = [float(n) for n in wine[1:14]]
            wine_params.append(params)
            species: int = int(wine[0])

            if species == 1:
                wine_class.append([1.0, 0.0, 0.0])
            elif species == 2:
                wine_class.append([0.0, 1.0, 0.0])
            else:
                wine_class.append([0.0, 0.0, 1.0])
            wine_species.append(species)
    feature_scaling(wine_params)

    nn: Network = Network([13, 7, 3], 0.9)
    x_train: List[List[float]] = wine_params[0:150]
    y_train: List[List[float]] = wine_class[0:150]

    for i in range(10):
        nn.train(x_train, y_train)
    
    x_test: List[List[float]] = wine_params[150:178]
    y_test: List[int] = wine_species[150:178]

    results: Tuple = nn.validate(x_test, y_test, interpret)
    print(f'{results[0]} correct of {results[1]} = {results[2] * 100}% ')