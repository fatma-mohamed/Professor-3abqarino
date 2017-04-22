from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess

class FeatureTwoSelector:
    
    def getRandomQuestion(self):
        row = DataAccess.DataAccess().selectRandom('''Questions_Answers''')
        return {
        "speech" : "",
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

    def CheckAnswerCorrectness(response):
        if response.get("result").get("parameters").get("correctAnsweID") == response.get("result").get(
                "parameters").get("chosenAnswer"):
            return {
                "speech": "Correct Answer :)",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "get-random-question",
                "followupEvent": {
                    "name": "Question_Answers"
                }
            }
        elif response.get("result").get("parameters").get("correctAnsweID") != response.get("result").get(
                "parameters").get("chosenAnswer"):
            return {
                "speech": "Wrong Answer :(",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "get-random-question",
                "followupEvent": {"name": "Question_Answers"}
            }





