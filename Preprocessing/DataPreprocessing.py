from Data.Database import Database
from NLP.TextParser import TextParser
from NLP.WordRecognizer import WordRecognizer

class DataPreprocessing:

    @staticmethod
    def insertAnswers_and_keywords():
        db = Database()
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
                keyword_id = db.select("Keywords", "id", "keyword", "'"+k+"'")
                if(keyword_id == None):
                    id = db.insert("Keywords", "keyword", "'"+k+"'", "keyword", "")
                    keywords_id.append(id)
                    synonyms = recognizer.getSynonym(k)
                    for s in synonyms:
                        db.insert("Synonyms", "key_id, synonym" , id + ", '"+s+"'" , "", "")
                else:
                    keywords_id.append(keyword_id)
            for id in keywords_id:
                print("K_ID: ", id)
                v = (str)(answer_id) + "," + (str)(id)
                db.insert("Answers_Keywords", "answer_id, keyword_id", v)