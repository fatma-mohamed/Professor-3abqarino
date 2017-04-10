from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess

class FeatureTwoSelector(ResponseSelector):
    
    def getRandomQuestion(self):
        row = DataAccess.getRandomQuestion()
        
        return {
        "speech" : "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "get-random-question",
        "followupEvent":{
            "name":"Question_Answers",
            "data":{
                "Question":row[0],
                "A1":row[1],
                "A2":row[2],
                "A3":row[3],
                "CA_ID":row[4]
                }
            }
        }
