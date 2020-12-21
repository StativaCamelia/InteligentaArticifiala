import numpy as np
from nltk import *
from nltk.corpus import stopwords
# import keras
# from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.python.keras.utils.np_utils import to_categorical


class VectorialRepresentation:
	def __init__(self):
		self.text_path = "text"
		self.content = ""
		self.words = []
		self.read_text()
		self.prepocesing()
		self.get_one_hot_vector()

	def read_text(self):
		with open(self.text_path) as text:
			self.content = text.read()

	def prepocesing(self):
		self.words = word_tokenize(self.content)
		self.words = [word.lower() for word in self.words if word.isalpha()]
		print(self.words)
		stop_words = set(stopwords.words('english'))
		self.words = [w for w in self.words if not w in stop_words]

	def get_one_hot_vector(self):
		#unique words
		self.dictionary = list(set(self.words))
		mapping = {}
		for x in range(len(self.dictionary)):
			mapping[self.dictionary[x]] = x
		for x in range(len(self.words)):
			self.words[x] = mapping[self.words[x]]
		one_hot_encode = to_categorical(self.words)

if  __name__ == "__main__":
	vect_repr = VectorialRepresentation()
