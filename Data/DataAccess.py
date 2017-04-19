from Data import Database

import psycopg2

class DataAccess:
    def selectRandom(self, tableName):
        conn = Database.Database()
        cur = conn.connection.cursor()
        print "--------Getting a random Question--------"
        cur.execute('''SELECT * FROM "''' + tableName +
                    '''" OFFSET floor(random()*(SELECT COUNT(*) FROM "''' + tableName + '''")) LIMIT 1''')
        rows = cur.fetchall()

        if tableName == '''Questions_Answers''':
            for row in rows:
                Question = row[1]
                print "Question = ", Question, "\n"
                A1 = row[2]
                print "A1 = ", A1, "\n"
                A2 = row[3]
                print "A2 = ", A2, "\n"
                A3 = row[4]
                print "A3 = ", A3, "\n"
                CA_ID = row[5]
                print "CA_ID = ", CA_ID, "\n"
            print "--------Got question--------"

        return rows[0]

    def select(self, table_name, cols, condition, value):
        conn = Database.Database()
        cur = conn.connection.cursor()
        if (condition == ""):
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''"''')
        else:
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''" WHERE ''' + condition + " = " + value)

        rows = cur.fetchall()
        conn.close()
        return rows
