from __future__ import annotations
from typing import List, Callable, Optional
from random import random
from neuron import Neuron
from util import dot_product


class Layer():
    def __init__(self,
                 prev_layer: Optional[Layer],
                 num_neurons: int,
                 learning_rate: float,
                 activation_function: Callable[[float], float],
                 derivative_function: Callable[[float], float]) -> None:
        self.prev_layer: Optional[Layer] = prev_layer
        self.neurons: List[Neuron] = []

        for _ in range(num_neurons):
            if prev_layer is None:
                random_weights: List[float] = []
            else:
                random_weights: List[float] = [random() for __ in range(len(prev_layer.neurons))]
            
            neuron: Neuron = Neuron(random_weights, learning_rate, activation_function, derivative_function)
            self.neurons.append(neuron)
        self.output_cache: List[float] = [0.0 for __ in range(num_neurons)]

    def outputs(self, inputs: List[float]) -> List[float]:
        self.output_cache: List[float]
        
        if self.prev_layer is None:
            self.output_cache = inputs
        else:
            self.output_cache = [n.output(inputs) for n in self.neurons]
        return self.output_cache
    
    def output_layer_deltas(self, expected: List[float]) -> None:
        for n in range(len(self.neurons)):
            _der: float = self.neurons[n].derivative_function(self.neurons[n].output_cache)
            self.neurons[n].delta: float = _der * (expected[n] - self.output_cache[n])
        
    def hidden_layer_deltas(self, next_layer: Layer) -> None:
        for idx, neuron in enumerate(self.neurons):
            next_weights: List[float] = [n.weights[idx] for n in next_layer.neurons]
            next_deltas: List[float] = [n.delta for n in next_layer.neurons]
            sum_weights_and_deltas: float = dot_product(next_weights, next_deltas)

            _dev: float = neuron.derivative_function(neuron.output_cache)
            neuron.delta: float = _dev * sum_weights_and_deltas
