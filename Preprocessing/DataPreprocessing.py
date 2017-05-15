from Data import *
from Preprocessing import config
from ResponseSelection import ResponseSelector

class DataPreprocessing:
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

    @staticmethod
    def insertGifs():
        db = Database()
        file = open("Preprocessing/gifs.txt", "r")

        while True:
            line = file.readline()
            if (line == ''):
                print("EOF!")
                break
            arr = line.split(" ")
            name = "'" + arr[0].strip("\n") + "'"
            url = "'" + arr[1].strip("\n") + "'"
            tag = "'" + arr[2].strip("\n") + "'"
            db.insert("Gifs", ["Name", "Url", "Tag"], [name, url, tag], "", "")

    @staticmethod
    def removeSinqleQuotes(s):
        res = s.replace("'", '"')
        return res

    def insertQuestions_Answers(self):
        f = open("Preprocessing/Question_Answers.txt", 'r')
        i=0
        while True:
            Question = f.readline().rstrip()
            if Question == "":
                print( "------Finished reading------")
                break
            A1 = f.readline().rstrip()
            A2 = f.readline().rstrip()
            A3 = f.readline().rstrip()
            CA_ID = f.readline().rstrip()
            cols = ["Question", "Answer_1", "Answer_2", "Answer_3", "Correct_AnswerID"]
            values=[ "'" + Question + "'" , "'" + A1 + "'" , "'" + A2 + "'" ,  "'" + A3 + "'" , "'" + str(CA_ID)+"'"]
            conflict_fields=["Question", "Answer_1", "Answer_2", "Answer_3", "Correct_AnswerID"]
            i += 1
            print ("-----Row " + (str)(i) + " -----")
            Database.Database().insert("Questions_Answers",cols,values,conflict_fields,'')

        return {
            "speech": "Inserted Questions_Answers rows",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "insert-Questions_Answers-rows"
        }

    def insertNotifications(self):
        f = open("Preprocessing/Notifications.txt", 'r')
        i = 0
        while True:
            Notification = f.readline().rstrip()
            if Notification == "":
                print("------Finished reading------")
                break

            cols = []
            values = []
            if "Attachment" in Notification:
                content = Notification.split(" Attachment: ")
                cols = ["Message", "Attachment"]
                values = ["'" + content[0] + "'", "'" + content[1] + "'"]
            else:
                cols = ["Message"]
                values = ["'" + Notification + "'"]
            conflict_fields = [""]
            i += 1
            print ("-----Notification number :: " + (str)(i) + " -----")
            Database.Database().insert("Notification", cols, values, conflict_fields, '')

        return {
            "speech": "Inserted Notification messages",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "insert-Notifications-rows"
        }
