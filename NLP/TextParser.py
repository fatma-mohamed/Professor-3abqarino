from nltk.tokenize import word_tokenize

class TextParser:

    def tokenize(input):
        list = word_tokenize(input)
        return list


    def extractKeywords(list):
        stopList = set(line.strip() for line in open('stoplist'))
        filtered_words = [word for word in list if word not in stopList]
        return filtered_words