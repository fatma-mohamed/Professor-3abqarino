from ResponseSelection.ResponseSelector import ResponseSelector
from Data import DataAccess
from random import randint

class FeatureTwoSelector:
    
    def getRandomQuestion(self,answerFeedback = "", imageURL = ""):
       row = DataAccess.DataAccess().selectRandom('''Questions_Answers''')
       # rows = DataAccess.DataAccess().selectGifsRandom("Questions_Answers",
       #                                                 ["Question", "Answer_1", "Answer_2", "Answer_3", "Correct_AnswerID"],
       #                                                 [], [], "")
       
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
                       "Question": row[0],
                       "A1": row[1],
                       "A2": row[2],
                       "A3": row[3],
                       "CA_ID": row[4],
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
                       "imageURL": imageURL
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
                rows = d.selectGifsRandom("Gifs" , ["url"] , ["tag"] , ["'correct'"], "")
                url = rows[0]
                return self.getRandomQuestion(answerFeedback="Correct Answer :)", imageURL=url)
        elif correctAnswer != chosenAnswer:
            if randomNum < 10:
                return self.getRandomQuestion(answerFeedback="Wrong Answer :(")
            else:
                d = DataAccess.DataAccess()
                rows = d.selectGifsRandom("Gifs" , ["url"] , ["tag"] , ["'incorrect'"], "")
                url = rows[0]
                return self.getRandomQuestion(answerFeedback="Wrong Answer :(", imageURL=url)




