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
            db.insert("Answers", "answer", "'" + answer + "'", "", "")
            answer_id = db_access.select("Answers", "id", "answer", "'" + answer + "'")
            tokens = parser.tokenize(question)
            keywords = parser.removeStopWords(tokens)
            keywords_id = []
            for k in keywords:
                keyword_id = db_access.select("Keywords", "id", "keyword", "'" + k + "'")
                if len(keyword_id) == 0:
                    db.insert("Keywords", "keyword", "'" + k + "'", "keyword", "")
                    id = db_access.select("Keywords", "id", "keyword", "'" + k + "'")
                    keywords_id.append(id[0][0])
                    synonyms = recognizer.getSynonym(k)
                    for s in synonyms:
                        z = str(id[0][0]) + ", '" + s + "'"
                        db.insert("Synonyms", "key_id, synonym", z, "", "")
                else:
                    keywords_id.append(keyword_id[0][0])
            for i in keywords_id:
                v = str(answer_id[0][0]) + "," + str(i)
                db.insert("Answers_Keywords", "answer_id, keyword_id", v, "answer_id, keyword_id", "")

    @staticmethod
    def removeSinqleQuotes(s):
        res = s.replace("'", '"')
        return res



    def insertQuestions_Answers(self):
        f = open("Question_Answers.txt", 'r')
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
            Database.Database().insert("Questions_Answers",
                                       "Question, Answer_1, Answer_2, Answer_3, Correct_AnswerID",
                                       "'" + Question + "'" + ", " + "'" + A1 + "'" + ", " + "'" + A2 + "'" + ", "
                                       + "'" + A3 + "'" + ", " + str(CA_ID),
                                       "Question, Answer_1, Answer_2, Answer_3, Correct_AnswerID",
                                       '')

        return {
            "speech": "Inserted Questions_Answers rows",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "insert-Questions_Answers-rows"
        }
