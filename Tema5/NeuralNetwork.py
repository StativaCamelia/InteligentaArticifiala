import math
import random

import numpy as np

def sigmoid_activation(z):
	return 1 / (1 + np.exp(-z))

class NeuralNetwork:
	def __init__(self, labels , learning_rate, number_of_epochs):
		self.no_of_epochs = number_of_epochs
		self.labels = labels
		self.learning_rate = learning_rate
		self.layers_sizes = [2, 2, 1]
		self.weights = []
		self.biases = []
		self.initialize_biases()
		self.initialize_weights()

	def initialize_weights(self):
		self.weights = [np.random.randn(self.layers_sizes[i], self.layers_sizes[i - 1]) for i in range(1, len(self.layers_sizes))]
		print(self.weights)

	def initialize_biases(self):
		self.biases = [np.random.randn(self.layers_sizes[i], 1) for i in range(1, len(self.layers_sizes))]

	def feed_forward(self, x):
		activations, net_inputs = [], []
		activation_predecesor = x.reshape(2, 1)
		activations.append(activation_predecesor)
		for i in range(len(self.layers_sizes) - 1):
			net_input = np.dot(self.weights[i], activation_predecesor) + self.biases[i]
			net_inputs.append(net_input.T)
			activation_predecesor = sigmoid_activation(net_input)
			activations.append(activation_predecesor.T)
		return net_inputs, activations

	def get_output(self, x):
		activation = x.reshape(2, 1)
		for i in range(len(self.layers_sizes) - 1):
			net_input = np.dot(self.weights[i], activation) + self.biases[i]
			activation = sigmoid_activation(net_input)
		return activation

	def error_last_layer(self, output, target):
		return self.sigmoid_derivative(output)*(output-target)

	def backward(self, net_inputs, activations, label):
		changes_w, changes_b = [np.zeros(w.shape) for w in self.weights], [np.zeros(b.shape) for b in self.biases]
		error = self.error_last_layer(activations[-1], label)
		changes_b[-1], changes_w[-1] = error, np.dot(error, activations[-2])
		sd = self.sigmoid_derivative(net_inputs[0])
		error = np.dot(self.weights[-1].T, error) * sd.T
		changes_b[0], changes_w[0] = error, np.dot(error,activations[0].T)
		return changes_b, changes_w

	@staticmethod
	def sigmoid_derivative(z):
		return sigmoid_activation(z) * (1 - sigmoid_activation(z))

	def get_inputs(self):
		return [np.array([0,0]), np.array([0,1]), np.array([1, 0]), np.array([1, 1])]

	def train(self):
		inputs = self.get_inputs()
		epoch = 0
		while epoch < self.no_of_epochs:
			results = []
			delta_w, delta_b = [np.zeros(w.shape) for w in self.weights], [np.zeros(b.shape) for b in self.biases]
			for i in range(4):
				net_inputs, activations = self.feed_forward(inputs[i])
				changes_b, changes_w = self.backward(net_inputs, activations, self.labels[i])
				delta_w = [dw + nw for dw, nw in zip(delta_w, changes_w)]
				delta_b = [db + nb for db, nb in zip(delta_b, changes_b)]
				results.append(self.get_output(inputs[i]))
			self.weights = [w - nw * (self.learning_rate/4) for w, nw in zip(self.weights, delta_w)]
			self.biases = [b - nb * (self.learning_rate/4) for b, nb in zip(self.biases, delta_b)]
			epoch += 1
			error = self.loss(results, self.labels)
			print(error)
		self.accuracy()

	def loss(self, y, t):
		return np.mean((np.array(t) - np.array(y)) ** 2)

	def accuracy(self):
		random.shuffle(self.get_inputs())
		results = [(x,0) if self.get_output(x) < 0.5 else (x, 1) for x in self.get_inputs()]
		print(results)
