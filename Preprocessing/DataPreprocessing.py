from Data.Database import Database
from Data.DataAccess import DataAccess
from NLP.TextParser import TextParser
from NLP.WordRecognizer import WordRecognizer

class DataPreprocessing:

    @staticmethod
    def insertAnswers_and_keywords():
        db = Database()
        db_access = DataAccess()
        parser = TextParser()
        recognizer  = WordRecognizer()
        file = open("Preprocessing/essay_questions.txt", "r")

        while True:
            line = file.readline()
            if (line == ''):
                print("no question!")
                break
            question = line.strip('-')
            line = file.readline()
            if (line == ''):
                print("no answer!")
                break
            answer = line.strip('\n')
            print("Question: ", question , "\nAnswer: ", answer)
            answer_id = db.insert("Answers", "answer", "'"+answer+"'", "" , "")
            tokens = parser.tokenize(question)
            keywords = parser.removeStopWords(tokens)
            keywords_id = []
            for k in keywords:
                print("Keyword: " , k)
                keyword_id = db_access.select("Keywords", "id", "keyword", "'"+k+"'")
                if keyword_id >= 0:
                    keywords_id.append(keyword_id)
                else:
                    id = db.insert("Keywords", "keyword", "'" + k + "'", "keyword", "")
                    keywords_id.append(id)
                    synonyms = recognizer.getSynonym(k)
                    for s in synonyms:
                        db.insert("Synonyms", "key_id, synonym", id + ", '" + s + "'", "", "")
            print("KEYWORDS: ", keywords_id)
            for i in keywords_id:
                print("K_ID: ", i)
                v = str(answer_id) + "," + str(i)
                db.insert("Answers_Keywords", "answer_id, keyword_id", v,"answer_id, keyword_id","")