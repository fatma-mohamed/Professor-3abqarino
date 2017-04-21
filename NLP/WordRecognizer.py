from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag, ne_chunk

class WordRecognizer:

    def getSynonym(word):
        list = set()
        for w in wn.synsets(word):
            list.add(w.lemmas()[0].name())
        return list

    def namedEntity(tokens):
        tags = pos_tag(tokens)
        ner = ne_chunk(tags)
        return ner
