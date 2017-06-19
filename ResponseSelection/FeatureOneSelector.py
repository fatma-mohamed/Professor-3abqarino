from NLP.TextParser import TextParser
from NLP.WordRecognizer import WordRecognizer
from Data import DataAccess
from collections import Counter
import requests


class FeatureOneSelector():
    question = ""

    def __init__(self, question):
        self.question = question


    def getResult(self):
        print ("QUES:", self.question)
        answer = self.getAnswer()
        if "Sorry" in answer:
            webAnswer = self.webSearch(self.question)
            print("WEB: ", webAnswer)
            if(webAnswer == 0):
                db = DataAccess.DataAccess()
                url = db.selectGifsRandom("Gifs", ["url"], ["gif_tag"], ["'question-mark'"], "")
                url = url[0][0]
                print("URL: ", url)
                return {
                    "speech": "",
                    "displayText": "",
                    "data": {},
                    "contextOut": [],
                    "source": "webhook-FeatureOneSelector",
                    "followupEvent": {"name": "ask_question_event",
                                      "data": {"imageURL": url, "speech": answer}}
                }
            else:
                icon = (webAnswer.get("Icon")).get("URL")
                text = webAnswer.get("Text")
                url = webAnswer.get("FirstURL")
                return {
                    "speech": "Sorry I couldn't find an answer! Here is a web search result",
                    "displayText": "",
                    "data": {},
                    "contextOut": [],
                    "source": "webhook-FeatureOneSelector",
                    "followupEvent": {"name": "ask_question_event",
                                      "data": {"imageURL": icon, "speech": text, "url": url}}
                }
        else:
            return {
                "speech": answer,
                "source": "webhook-FeatureOneSelector",
                "displayText": answer

            }

    def getAnswer(self):
        Tx = TextParser()
        t = Tx.tokenize(self.question)
        k = Tx.removeStopWords(t)
        keywordsID = self.retriveSynonymID(k)
        # ner = WordRecognizer.namedEntity(k)
        mostCommenAnswers = self.retriveAnswersID(keywordsID)
        if len(mostCommenAnswers) == 0:
            return "Sorry I have no answers to this question!"
        answer = self.retriveAnswer(mostCommenAnswers)
        print (answer)
        print ("__________")
        print (answer [0])
        print("_______")
        print (answer[0][0])
        return answer[0][0]

    def retriveSynonymID(self, keywords):
        synonymKey = []
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

    def webSearch(self, query):
        Tx = TextParser()
        t = Tx.tokenize(query.lower())
        k = Tx.removeStopWords(t)
        query = ''.join(k)
        if query == '':
            print ("NO QUERY")
            return 0
        print ("Q:", query)
        url = "http://api.duckduckgo.com/?q=" + query \
              + "&format=json&pretty=1"
        response = requests.get(url)
        jData = response.json()
        results = jData.get("RelatedTopics")
        print("RES: ",results)
        if len(results)==0:
            print("JSON: ", 0)
            return 0
        first = results[0]
        print("JSON: ", first)
        return first


