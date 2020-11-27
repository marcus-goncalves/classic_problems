from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivative_sigmoid


T = TypeVar('T')

class Network():
    def __init__(self,
                 layer_structure: List[int],
                 learning_rate: float,
                 activation_function: Callable[[float], float] = sigmoid,
                 derivative_function: Callable[[float], float] = derivative_sigmoid) -> None:
        if len(layer_structure) < 3:
            raise ValueError('Error: Should be at least 3 layers')
        
        self.layers: List[Layer] = []
        input_layer: Layer = Layer(None, layer_structure[0], learning_rate, 
                                   activation_function, derivative_function)
        self.layers.append(input_layer)

        for previous, num_neurons in enumerate(layer_structure[1::]):
            next_layer = Layer(self.layers[previous], num_neurons,
                               learning_rate, activation_function, derivative_function)
            self.layers.append(next_layer)

    def outputs(self, _input: List[float]) -> List[float]:
        return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, _input)

    def backpropagate(self, expected: List[float]) -> None:
        last_layer: int = len(self.layers) - 1
        self.layers[last_layer].output_layer_deltas(expected)

        for i in range(last_layer - 1, 0, -1):
            self.layers[i].hidden_layer_deltas(self.layers[i + 1])

    def update_weights(self) -> None:
        for Layer in self.layers[1:]:
            for neuron in Layer.neurons:
                for w in range(len(neuron.weights)):
                    _dev: float = neuron.learning_rate * (Layer.prev_layer.output_cache[w]) * neuron.delta
                    neuron.weights[w] = neuron.weights[w] + _dev
    
    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        for location, xs in enumerate(inputs):
            ys: List[float] = expecteds[location]
            # self.outputs(xs)
            outs: List[float] = self.outputs(xs)
            self.backpropagate(ys)
            self.update_weights()
    
    def validate(self, 
                 inputs: List[List[float]], 
                 expecteds: List[T],
                 interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
        correct: int = 0

        for _input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(_input))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage