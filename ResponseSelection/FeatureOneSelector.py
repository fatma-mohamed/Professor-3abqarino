from ResponseSelection.ResponseSelector import ResponseSelector
from NLP import *
from Data import DataAccess
from collections import Counter


class FeatureOneSelector(ResponseSelector):
    question = ""

    def __init__(self, question):
        self.question = question

    def getAnswer(self):
        t = TextParser.tokenize(self.question)
        k = TextParser.extractKeywords(t)
        keywordsID = self.retriveSynonymID(k)
        # ner = WordRecognizer.namedEntity(k)
        mostCommenAnswers = self.retriveAnswersID(keywordsID)
        if len(mostCommenAnswers) == 0:
            return False
        answer = self.retriveAnswer(mostCommenAnswers)
        return answer

    def retriveSynonymID(self, keywords):
        synonymKey = []
        for word in keywords:
            Da = DataAccess.DataAccess()
            ids = Da.select("Synonyms", "key_id", "synonym =" + word)
            synonymKey += ids
            # for  id  in ids:
            #     keyWord =Da.select("Keywords","keyword","id = "+id)
            #     synonymKey.append(keyWord)

        return synonymKey

    def retriveAnswersID(self, keywordsIDs):
        Da = DataAccess.DataAccess()
        answersID = []
        for id in keywordsIDs:
            ids = Da.select("Answers_Keywords", "answer_id", "keyword_id = " + id)
            answersID += ids

        return Counter(answersID).most_common(3)

    def retriveAnswer(self, IDs):
        Da = DataAccess.DataAccess()
        Answer = Da.select("Answers", "Answers", "id = " + IDs[0][0])
        return Answer
