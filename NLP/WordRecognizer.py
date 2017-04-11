from nltk.corpus import wordnet as wn
class WordRecognizer:
    dummy_data = "dummy_data"
	
	def getSynonym(word):
		list = []
		for w in wn.synsets(word):
			list.append(w.lemmas()[0].name())
		return list
