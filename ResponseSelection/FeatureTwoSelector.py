from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess
from random import randint

class FeatureTwoSelector:
    
    def getRandomQuestion(self,answerFeedback = "", imageURL = ""):
        row = DataAccess.DataAccess().selectRandom('''Questions_Answers''')
        if imageURL == "":
            return {
                "speech": "",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "get-random-question",
                "followupEvent": {
                    "name": "Question_Answers",
                    "data": {
                        "Question": row[1],
                        "A1": row[2],
                        "A2": row[3],
                        "A3": row[4],
                        "CA_ID": row[5],
                        "AnswerFeedback": answerFeedback
                    }
                }
            }
        else:
            return {
                "speech": "",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "get-random-question",
                "followupEvent": {
                    "name": "Question_Answers",
                    "data": {
                        "Question": row[1],
                        "A1": row[2],
                        "A2": row[3],
                        "A3": row[4],
                        "CA_ID": row[5],
                        "AnswerFeedback": answerFeedback,
                        "imageURL" : imageURL
                    }
                }
            }

    def CheckAnswerCorrectness(self,request):
        correctAnswer= request.get("correctAnswerID")
        chosenAnswer= str(request.get("chosenAnswer"))
        randomNum = randint(0,19)
        if correctAnswer == chosenAnswer:
            if randomNum < 10:
                return self.getRandomQuestion(answerFeedback="Correct Answer :)")
            else:
                d = DataAccess.DataAccess()
                url = d.selectRandom("Gifs" , ["url"] , ["gif_tag"] , ["'correct'"], "")
                url = url[0][0]
                return self.getRandomQuestion(answerFeedback="Correct Answer :)", imageURL=url)
        elif correctAnswer != chosenAnswer:
            return

    def getCorrectAnswer(self, request):
        question = request.get("sentQuestion")
        CA_ID = request.get("CA_ID")
        print "-------Sent Question :: ", question
        print "---------CA_ID :: ", CA_ID
        CA_ID = CA_ID[:CA_ID.find(".") - len(CA_ID)] #Remove .0 ,, CA_ID = 1.0 or 2.0 or 3.0
        row = DataAccess.DataAccess().select("Questions_Answers", ["Answer_" + CA_ID], ["Question"], ["'" + question + "'"], '')
        answer = row[0][0]
        return {
            "speech": "",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "get-correct-answer",
            "followupEvent": {
                "name": "Cant_Answer",
                "data": {
                    "Answer": answer
                }
            }
        }

