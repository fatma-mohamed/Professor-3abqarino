from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag, ne_chunk
import TextParser
class WordRecognizer:
    dummy_data = "dummy_data"
	
	def getSynonym(word):
		list = []
		for w in wn.synsets(word):
			list.append(w.lemmas()[0].name())
		return list


	def namedEntity(sentence):
	    tokns= tokenize(sentence)
	    tags = pos_tag(tokns)
	    ner= ne_chunk(tags)
	    return ner

