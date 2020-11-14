from NeuralNetwork import NeuralNetwork
import numpy

number_of_epochs = int(input("Introduceti numarul de epoci de antrenare:"))
learning_rate = float(input("Introduceti rata de invatare:"))
function_results_str = input("Introduceti rezultatele functiei:")
function_results = [int(i) for i in function_results_str.split()]
neuralNetwork = NeuralNetwork(function_results, learning_rate, number_of_epochs)
neuralNetwork.train()