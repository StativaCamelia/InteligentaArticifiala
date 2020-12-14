import json

from nltk import *
from nltk.corpus import stopwords


def read_text(file):
	with open(file) as txt:
		return txt.read()


def prepocesing(file):
	words = word_tokenize(file)
	words = [word.lower() for word in words if word.isalpha()]
	stop_words = set(stopwords.words('romanian'))
	return [w for w in words if w not in stop_words]


def word_count(model_file, words):
	counts = dict()
	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	counts = {key: (counts[key] / len(words)) * 1000000 for key in counts}
	with open(model_file, "w") as fp:
		json.dump(counts, fp)


def sim_score(file1, file2):
	with open(file1, "r") as f1, open(file2, "r") as f2:
		content1 = json.load(f1)
		content2 = json.load(f2)
	suma = 0
	for word in content2:
		if word in content1:
			suma += abs(content2[word] - content1[word])
	print("Scor de similitudine: " + str(suma))
	print("Media diferenței: " + str(suma / len(content2)))


if __name__ == '__main__':
	eminescu_file_content = read_text("MihaiEminescu")
	eminescu_file_without_stop = prepocesing(eminescu_file_content)
	word_count("eminescu_lang_model.json", eminescu_file_without_stop)
	other_file_content = read_text("CreierulOEnigma")
	other_file_without_stop = prepocesing(other_file_content)
	word_count("creierul_lang_model.json", other_file_without_stop)
	sim_score("eminescu_lang_model.json", "creierul_lang_model.json")
