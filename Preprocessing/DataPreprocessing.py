from Data import *
from NLP.TextParser import TextParser

class DataPreprocessing:

    @staticmethod
    def __run__(self):
        self.insertAnswers_and_keywords()

    def insertAnswers_and_keywords(self):
        file = open("essay_questions.txt", "r")

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
            answer = line
            answer_id = Database.insert("Answers", "answer", answer)
            tokens = TextParser.tokenize(question)
            keywords = TextParser.removeStopWords(tokens)
            keywords_id = []
            for k in keywords:
                keywords_id.append(Database.insert("Keywords", "keyword", k))
            for id in keywords_id:
                v = (str)(answer_id) + "," + (str)(id)
                Database.insert("Answers_Keywords", "answer_id, keyword_id", v)