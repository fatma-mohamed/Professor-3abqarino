from Data import *

class DataPreprocessing:
    def __init__(self):
        return

    @staticmethod
    def __run__(self, db):
        db.__createTables__()

        return {
            "speech": "Created tables",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "create-database"
        }

        ##rest of the preprocessing

    def insertQuestions_Answers(self):
        ff = open("requirements.txt", 'r')
        f = open('''Question_Answers.txt''', 'r')
        i=0
        while True:
            Question = f.readline().rstrip()
            if Question == "":
                print "------Finished reading------"
                break
            A1 = f.readline().rstrip()
            A2 = f.readline().rstrip()
            A3 = f.readline().rstrip()
            CA_ID = f.readline().rstrip()

            i += 1
            print "-----Row " + (str)(i) + " -----"
            DataAccess.insertQuestion_Answers(Question, A1, A2, A3, CA_ID)

        return {
            "speech": "Inserted Questions_Answers rows",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "insert-Questions_Answers-rows"
        }
