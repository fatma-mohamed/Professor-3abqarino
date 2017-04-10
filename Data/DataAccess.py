import psycopg2

class DataAccess:

    def getRandomQuestion(self):
        conn = Database.Database()
        cur = conn.cursor()
        print "--------Getting a random Question--------"
        cur.execute("SELECT * FROM "Questions_Answers" OFFSET floor(random()*(SELECT COUNT(*) FROM "Questions_Answers")) LIMIT 1")
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
