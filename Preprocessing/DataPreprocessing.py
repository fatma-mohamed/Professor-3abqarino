from Data.Database import Database
from Data.DataAccess import DataAccess
from NLP.TextParser import TextParser
from NLP.WordRecognizer import WordRecognizer


class DataPreprocessing:


    def __run__(self, db):
        db.__createTables__()

        return {
            "speech": "Created tables",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "create-database"
        }

    @staticmethod
    def insertAnswers_and_keywords():
        db = Database()
        db_access = DataAccess()
        parser = TextParser()
        recognizer = WordRecognizer()
        file = open("Preprocessing/essay_questions.txt", "r")

        while True:
            line = file.readline()
            if (line == ''):
                print("no question!")
                break
            question = DataPreprocessing.removeSinqleQuotes(line.strip('-'))
            line = file.readline()
            if (line == ''):
                print("no answer!")
                break
            answer = DataPreprocessing.removeSinqleQuotes(line.strip('\n'))
            cols = ["answer"]
            values = ["'" + answer + "'"]
            db.insert("Answers", cols, values, "", "")

            cols = ["id"]
            parameters = ["answer"]
            values = ["'" + answer + "'"]
            answer_id = db_access.select("Answers", cols, parameters, values, "")

            tokens = parser.tokenize(question)
            keywords = parser.removeStopWords(tokens)
            keywords_id = []
            for k in keywords:

                cols = ["id"]
                parameters = ["keyword"]
                values = [ "'" + k + "'"]
                keyword_id = db_access.select("Keywords", cols, parameters,values,"")
                if len(keyword_id) == 0:
                    cols = ["keyword"]
                    values = ["'" + k + "'"]
                    conflict_fields = ["keyword"]
                    db.insert("Keywords", cols, values, conflict_fields, "")

                    cols = ["id"]
                    parameters = ["keyword"]
                    values = ["'" + k + "'"]
                    id = db_access.select("Keywords", cols, parameters, values, "")
                    keywords_id.append(id[0][0])
                    synonyms = recognizer.getSynonym(k)
                    for s in synonyms:
                        cols = ["key_id", "synonym"]
                        values = [str(id[0][0]) + ", '" + s + "'"]
                        db.insert("Synonyms", cols, values, "", "")
                else:
                    keywords_id.append(keyword_id[0][0])
            for i in keywords_id:
                cols = ["answer_id", "keyword_id"]
                values = [str(answer_id[0][0]) + "," + str(i)]
                conflict_fields = ["answer_id", "keyword_id"]
                db.insert("Answers_Keywords", cols, values, conflict_fields, "")

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
            db.insert("Tag",["tag"],[tag],["tag"],"")
            db.insert("Gifs", ["Name", "Url" , "Tag"], [name,url,tag],"","")

    @staticmethod
    def removeSinqleQuotes(s):
        res = s.replace("'", '"')
        return res
