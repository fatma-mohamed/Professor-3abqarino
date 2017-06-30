from Data.Database import Database
from Data.DataAccess import DataAccess

class DataPreprocessing:
    def __run__(self):
        d = Database()
        d.__deleteTables__()
        d.__createTables__()
        self.insertQuestions_Answers()
        self.insertGifs()
        self.insertNotifications()
        print("Data preprocessing done!")

    def insertQuestions_Answers(self):
        db = Database()
        f = open("Preprocessing/Question_Answers.txt", 'r')
        i = 0
        while True:
            Question = DataPreprocessing.removeSinqleQuotes(f.readline().rstrip())
            if Question == "":
                print("------Finished reading------")
                break
            A1 = DataPreprocessing.removeSinqleQuotes(f.readline().rstrip())
            A2 = DataPreprocessing.removeSinqleQuotes(f.readline().rstrip())
            A3 = DataPreprocessing.removeSinqleQuotes(f.readline().rstrip())
            CA_ID = f.readline().rstrip()
            cols = ["Question", "Answer_1", "Answer_2", "Answer_3", "Correct_AnswerID"]
            values = ["'" + Question + "'", "'" + A1 + "'", "'" + A2 + "'", "'" + A3 + "'", "'" + str(CA_ID) + "'"]
            conflict_fields = ["Question", "Answer_1", "Answer_2", "Answer_3", "Correct_AnswerID"]
            i += 1
            print ("-----Row " + (str)(i) + " -----")
            db.insert("Questions_Answers", cols, values, conflict_fields, '')
        print ("Inserted Questions_Answers rows")

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
            db.insert("Tag", ["tag"], [tag], ["tag"], "")
            db.insert("Gifs", ["name", "url", "gif_tag"], [name, url, tag], "", "")
        print ("Inserted Tags & Gifs")

    @staticmethod
    def insertNotifications():
        db = Database()
        db_access = DataAccess()
        f = open("Preprocessing/Notifications.txt", 'r')
        i = 0
        while True:
            Notification = DataPreprocessing.removeSinqleQuotes(f.readline().rstrip())
            if Notification == "":
                print("------Finished reading------")
                break

            cols = []
            values = []
            noAttachment = True
            if "Attachment" in Notification:
                content = Notification.split(" Attachment: ")
                rows = db_access.select("Tag", ["Tag"], ["Tag"], ["'" + content[1] + "'"], "")
                row = rows[0][0]
                if row is not None:  # Check the existence of the tag used as an attachment.
                    cols = ["Message", "Attachment"]
                    values = ["'" + content[0] + "'", "'" + content[1] + "'"]
                    noAttachment = False
                else:  # Tag doesn't exist ,, Modify Notification text to be inserted using next if condition.
                    Notification = content[0]
            if noAttachment == True:
                cols = ["Message"]
                values = ["'" + Notification + "'"]
            conflict_fields = ["Message"]
            i += 1
            print ("-----Notification number :: " + (str)(i) + " -----")
            db.insert("Notification", cols, values, conflict_fields, "")
        print ("Inserted Notification messages")

    @staticmethod
    def removeSinqleQuotes(s):
        res = s.replace("'", '"')
        return res

    @staticmethod
    def addSinqleQuotes(s):
        res = s.replace('"', "'")
        return res
