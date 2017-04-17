from Data import *

class DataPreprocessing:
    def __init__(self):
        return

    @staticmethod
    def __run__(self, db):
        return db.__createTables__()

        ##rest of the preprocessing

    def insertQuestions_Answers(self):
        f = open("Questions_Answers.txt", 'r')
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

        return
