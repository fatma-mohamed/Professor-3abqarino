from Data import Database

import psycopg2

class DataAccess:
    def insertQuestion_Answers(self, Question, A1, A2, A3, CA_ID):
        conn = Database.Database()
        cur = conn.connection.cursor()
        print "--------Adding question to DB--------"
        cur.execute('''INSERT INTO "Questions_Answers" (Question, Answer_1, Answer_2, Answer_3, Correct_AnswerID) VALUES (''' + "'" + Question + "'" + ", " + "'" + A1 + "'" + ", " + "'" + A2 + "'" + ", " + "'" + A3 + "'" + ", " + (str)(CA_ID) + ");")
        conn.connection.commit()
        print "--------Rows inserted--------"
        return

    def getRandomQuestion(self):
        conn = Database.Database()
        cur = conn.connection.cursor()
        print "--------Getting a random Question--------"
        cur.execute('''SELECT * FROM "Questions_Answers" OFFSET floor(random()*(SELECT COUNT(*) FROM "Questions_Answers")) LIMIT 1''')
        rows = cur.fetchall()

        for row in rows:
            Question = row[0]
            print "Question = ", Question, "\n"
            A1 = row[1]
            print "A1 = ", A1, "\n"
            A2 = row[2]
            print "A2 = ", A2, "\n"
            A3 = row[3]
            print "A3 = ", A3, "\n"
            CA_ID = row[4]
            print "CA_ID = ", CA_ID, "\n"
        print "--------Got question--------"

        return rows
