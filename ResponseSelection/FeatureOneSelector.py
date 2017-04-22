from NLP.TextParser import TextParser
from ResponseSelection.ResponseSelector import ResponseSelector
from NLP import TextParser,WordRecognizer
from Data import DataAccess
from collections import Counter


class FeatureOneSelector(ResponseSelector):
    question = ""

    def __init__(self, question):
        self.question = question

    def getAnswer(self):
        Tx = TextParser.TextParser()
        t = Tx.tokenize(self.question)
        k = Tx.removeStopWords(t)
        keywordsID = self.retriveSynonymID(k)
        # ner = WordRecognizer.namedEntity(k)
        mostCommenAnswers = self.retriveAnswersID(keywordsID)
        if len(mostCommenAnswers) == 0:
            return "sorry i have no answers to this question ! :("
        answer = self.retriveAnswer(mostCommenAnswers)
        return answer

    def retriveSynonymID(self, keywords):
        synonymKey = []
        Da = DataAccess.DataAccess()
        for word in keywords:
            w="'"+word+"'"
            word =w
            ids = Da.select("Synonyms", "key_id", "synonym =" + word)
            synonymKey += ids
            # for  id  in ids:
            #     keyWord =Da.select("Keywords","keyword","id = "+id)
            #     synonymKey.append(keyWord)

        return synonymKey

    def retriveAnswersID(self, keywordsIDs):
        Da = DataAccess.DataAccess()
        answersID = []
        print ("________in retriveAnswersID _______________ ")
        print(keywordsIDs)
        for id in keywordsIDs:
            ids = Da.select("Answers_Keywords", "answer_id", "keyword_id = " + str(id[0]))
            answersID += ids
        return Counter(answersID).most_common(3)

    def retriveAnswer(self, IDs):
        Da = DataAccess.DataAccess()
        print (IDs)
        Answer = Da.select("Answers", "answer", "id = " + str(IDs[0][0][0]))
        return Answer
