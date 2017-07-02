from NLP.TextParser import TextParser
from NLP.WordRecognizer import WordRecognizer
from Preprocessing.DataPreprocessing import DataPreprocessing
import ResponseSelection
from Data import DataAccess
from collections import Counter


class FeatureOneSelector():
    question = ""

    def __init__(self, question):
        self.question = question.lower()


    def getResult(self):
        print ("QUES:", self.question)
        answer = self.getAnswer()
        if "Sorry" in answer:
            res = ResponseSelection.ResponseSelector.ResponseSelector()
            webAnswer = res.webSearch(self.question)
            print("WEB: ", webAnswer)
            if not webAnswer.get("data"):
                db = DataAccess.DataAccess()
                url = db.selectRandom("Gifs", ["url"], ["gif_tag"], ["'question-mark'"], "")
                url = url[0][0]
                print("URL: ", url)
                return {
                    "speech": answer,
                    "displayText": "",
                    "data": {
                        "facebook": [
                            {
                                "text" : answer
                            },
                            {
                                "attachment": {
                                    "type": "image",
                                    "payload": {
                                        "url": url
                                    }
                                }
                            }
                        ]
                    },
                    "contextOut": [],
                    "source": "webhook-FeatureOneSelector-getResult"
                }
            else:
                return webAnswer
        else:
            return {
                "speech": DataPreprocessing.addSinqleQuotes(answer),
                "source": "webhook-FeatureOneSelector-getResult"
            }

    def getAnswer(self):
        Tx = TextParser()
        t = Tx.tokenize(self.question)
        k = Tx.removeStopWords(t)
        keywordsID = self.retriveSynonymID(k)
        # ner = WordRecognizer.namedEntity(k)
        mostCommenAnswers = self.retriveAnswersID(keywordsID)
        print("MM:" , mostCommenAnswers)
        if len(mostCommenAnswers) == 0:
            return "Sorry I have no answers to this question!"
        elif  mostCommenAnswers[0][1] < 3:
            return "Sorry I have no answers to this question!"
        answer = self.retriveAnswer(mostCommenAnswers)
        print (answer)
        print ("__________")
        print (answer [0])
        print("_______")
        print (answer[0][0])
        return answer[0][0]

    def retriveSynonymID(self, keywords):
        synonymKey = keywords
        Da = DataAccess.DataAccess()
        for word in keywords:
            w="'"+word+"'"
            word =w
            ids = Da.select("Synonyms", ["key_id"], ["synonym"],[word],"")
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
            ids = Da.select("Answers_Keywords", ["answer_id"], ["keyword_id"] , [str(id[0])],"")
            answersID += ids
        return Counter(answersID).most_common(3)

    def retriveAnswer(self, IDs):
        Da = DataAccess.DataAccess()
        print (IDs)
        Answer = Da.select("Answers", ["answer"], ["id"] , [str(IDs[0][0][0])],"")
        return Answer




