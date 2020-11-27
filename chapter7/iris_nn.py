import csv
from typing import List
from util import feature_scaling
from network import Network
from random import shuffle


def interpret_output(output: List[float]) -> str:
    if max(output) == output[0]:
        return 'Iris-setosa'
    elif max(output) == output[1]:
        return 'Iris-versicolor'
    else:
        return 'Iris-virginica'

if __name__ == "__main__":
    iris_parameters: List[List[float]] = []
    iris_classifications: List[List[float]] = []
    iris_species: List[str] = []

    with open('iris.data', 'r') as file:
        list_iris: List = list(csv.reader(file))
        shuffle(list_iris)

        for iris in list_iris:
            params: List[float] = [float(n) for n in iris[0:4]]
            iris_parameters.append(params)
            species: str = iris[4]

            if species == 'Iris-setosa':
                iris_classifications.append([1.0, 0.0, 0.0])
            elif species == 'Iris-versicolor':
                iris_classifications.append([0.0, 1.0, 0.0])
            else:
                iris_classifications.append([0.0, 0.0, 1.0])
            iris_species.append(species)
    feature_scaling(iris_parameters)

    iris_nn: Network = Network([4, 6, 3], 0.3)

    

    iris_trainers: List[List[float]] = iris_parameters[0:140]
    iris_trainers_correct: List[List[float]] = iris_classifications[0:140]

    for _ in range(50):
        iris_nn.train(iris_trainers, iris_trainers_correct)
    
    # Testing results
    iris_testers: List[List[float]] = iris_parameters[140:150]
    iris_testers_correct: List[str] = iris_species[140:150]
    results = iris_nn.validate(iris_testers, iris_testers_correct, interpret_output)

    print(f'{results[0]} correct of {results[1]} = {results[2] * 100}%  ')