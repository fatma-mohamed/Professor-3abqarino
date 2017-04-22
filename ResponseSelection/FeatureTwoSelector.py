

from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess

class FeatureTwoSelector:
    
    def getRandomQuestion(self,answerFeedback = ""):
        row = DataAccess.DataAccess().selectRandom('''Questions_Answers''')
        return {
        "speech" : answerFeedback,
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "get-random-question",
        "followupEvent":{
            "name":"Question_Answers",
            "data":{
                "Question": row[1],
                "A1": row[2],
                "A2": row[3],
                "A3": row[4],
                "CA_ID": row[5]
                }
            }
        }

    def CheckAnswerCorrectness(self,response):
        if response.get("result").get("parameters").get("correctAnswerID") == response.get("result").get(
                "parameters").get("chosenAnswer"):
            return self.getRandomQuestion("Correct Answer :)")

        elif response.get("result").get("parameters").get("correctAnswerID") != response.get("result").get(
                "parameters").get("chosenAnswer"):
            return self.getRandomQuestion("Wrong Answer :(")




