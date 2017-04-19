from Data import *
from NLP.TextParser import TextParser

class DataPreprocessing:

    @staticmethod
    def insertAnswers_and_keywords():
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
            answer = line
            print("Question: ", question , "\nAnswer: ", answer)
            answer_id = Database.insert("Answers", "answer", answer)
            tokens = TextParser.tokenize(question)
            keywords = TextParser.removeStopWords(tokens)
            keywords_id = []
            for k in keywords:
                print("Keyword: " , k)
                keywords_id.append(Database.insert("Keywords", "keyword", k))
            for id in keywords_id:
                print("K_ID: ", id)
                v = (str)(answer_id) + "," + (str)(id)
                Database.insert("Answers_Keywords", "answer_id, keyword_id", v)