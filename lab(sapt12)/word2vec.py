from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import numpy as np
import string


def softmax(x):
	e_x = np.exp(x - np.max(x))
	return e_x / e_x.sum()


class VectorialRepresentation:
	def __init__(self):
		self.text_path = "text"
		self.content = ""
		self.alpha = 0.1
		self.training_input = []
		self.window_size = 2
		self.X_train = []
		self.Y_train = []
		self.N = 10
		self.words = []
		self.word_index = {}
		self.epochs = 20
		self.read_text()
		self.preprocessing()
		self.prepare_data_for_training()

	def read_text(self):
		with open(self.text_path) as text:
			self.content = text.read()

	def preprocessing(self):
		stop_words = set(stopwords.words('english'))
		sentences = self.content.split(".")
		self.words = []
		for i in range(len(sentences)):
			sentence = sentences[i].strip().split()
			x = [word.strip(string.punctuation).lower() for word in sentence if word not in stop_words]
			[self.words.append(word) for word in x]
			self.training_input.append(x)

	def prepare_data_for_training(self):
		data = {}
		for sentence in self.training_input:
			for word in sentence:
				if word not in data:
					data[word] = 1
				else:
					data[word] += 1
		V = len(data)
		data = sorted(list(data.keys()))
		vocab = {}
		for i in range(len(data)):
			vocab[data[i]] = i
		for sentence in self.training_input:
			for i in range(len(sentence)):
				center_word = [0 for _ in range(V)]
				center_word[vocab[sentence[i]]] = 1
				context = [0 for _ in range(V)]
				for j in range(i - self.window_size, i + self.window_size):
					if i != j and 0 <= j < len(sentence):
						context[vocab[sentence[j]]] += 1
				self.X_train.append(center_word)
				self.Y_train.append(context)
		self.initialize(V, data)

	def initialize(self, V, data):
		self.V = V
		self.W = np.random.uniform(-0.8, 0.8, (self.V, self.N))
		self.W1 = np.random.uniform(-0.8, 0.8, (self.N, self.V))
		self.words = data
		for i in range(len(data)):
			self.word_index[data[i]] = i

	def feed_forward(self, X):
		self.h = np.dot(self.W.T, X).reshape(self.N, 1)
		self.u = np.dot(self.W1.T, self.h)
		self.y = softmax(self.u)
		return self.y

	def backpropagate(self, x, t):
		# error final layer
		e = self.y - np.asarray(t).reshape(self.V, 1)
		dLdW1 = np.dot(self.h, e.T)
		# error hidden layer
		X = np.array(x).reshape(self.V, 1)
		dLdW = np.dot(X, np.dot(self.W1, e).T)
		# update weights
		self.W1 = self.W1 - self.alpha * dLdW1
		self.W = self.W - self.alpha * dLdW

	def train(self):
		for x in range(1, self.epochs):
			self.loss = 0
			for j in range(len(self.X_train)):
				self.feed_forward(self.X_train[j])
				self.backpropagate(self.X_train[j], self.Y_train[j])
				C = 0
				for m in range(self.V):
					if self.Y_train[j][m]:
						self.loss += -1 * self.u[m][0]
						C += 1
				self.loss += C * np.log(np.sum(np.exp(self.u)))
			print("epoch ", x, " loss = ", self.loss)
			self.alpha *= 1 / (1 + self.alpha * x)

	def predict(self, word, number_of_predictions):
		if word in self.words:
			index = self.word_index[word]
			X = [0 for _ in range(self.V)]
			X[index] = 1
			prediction = self.feed_forward(X)
			output = {}
			for i in range(self.V):
				output[prediction[i][0]] = i
			top_context_words = []
			out_top = []
			for k in sorted(output, reverse=True):
				top_context_words.append(self.words[output[k]])
				out_top.append(k)
				if len(top_context_words) >= number_of_predictions:
					break
			return top_context_words, out_top
		else:
			print("Word not found in dicitonary")

	def tsne_plot(self):
		labels = []
		tokens = []
		for word in self.words:
			tokens.append(self.predict(word, 10)[1])
			labels.append(word)
		tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
		new_values = tsne_model.fit_transform(tokens)
		x = []
		y = []
		for value in new_values:
			x.append(value[0])
			y.append(value[1])
		plt.figure(figsize=(12, 8))
		for i in range(len(x)):
			plt.scatter(x[i], y[i])
			plt.annotate(labels[i],xy=(x[i], y[i]),xytext=(5, 2),
					 textcoords='offset points',
					 ha='right',
					 va='bottom')
		plt.show(block=False)
		plt.show()

word2vec = VectorialRepresentation()
word2vec.train()
words = ["december", "religious", "solstice"]
word2vec.tsne_plot()
for word in words:
	print(word2vec.predict(word, 2))
