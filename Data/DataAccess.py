from Data import Database

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

    def selectRandom(self, table_name, cols, parameters, values, operators):
        db = Database.Database()
        cur = db.connection.cursor()
        if (isinstance(cols, list)):
            cols_str = ""
            cols_size = len(cols)
            for i in range(0, cols_size):
                if i == cols_size - 1:
                    cols_str += str(cols[i])
                    break
                cols_str += (str(cols[i]) + ", ")
        else:
            cols_str = "*"

        if (not parameters):
            cur.execute('''SELECT ''' + cols_str + ''' FROM "''' + table_name +
                        '''" ORDER BY RANDOM() limit 1;''')
        else:
            parameters_size = len(parameters)
            conditions = ""
            for j in range(0, parameters_size):
                if j == parameters_size - 1:
                    conditions += (str(parameters[j]) + " = " + str(values[j]))
                    break
                conditions += (str(parameters[j]) + " = " + str(values[j]) + " " + str(operators[j]) + " ")

            cur.execute('''SELECT ''' + cols_str + ''' FROM "''' + table_name +
                        '''" WHERE ''' + conditions + ''' ORDER BY RANDOM() limit 1;''')
        rows = cur.fetchall()
        cur.close()
        return rows

    def select(self, table_name, cols, parameters, values , operators):
        db = Database.Database()
        cur = db.connection.cursor()
        if (isinstance(cols, list)):
            cols_str = ""
            cols_size = len(cols)
            for i in range(0, cols_size):
                if i == cols_size - 1:
                    cols_str += str(cols[i])
                    break
                cols_str += (str(cols[i]) + ", ")
        else:
            cols_str = "*"

        if (not parameters):
            cur.execute("SELECT " + cols_str + ''' from "''' + table_name + '''"''')
        else:
            parameters_size = len(parameters)
            conditions = ""
            for j in range(0, parameters_size):
                if j == parameters_size - 1:
                    conditions += (str(parameters[j]) + " = " + str(values[j]))
                    break
                conditions += (str(parameters[j]) + " = " + str(values[j]) + " " + str(operators[j]) + " ")
            cur.execute("SELECT " + cols_str + ''' from "''' + table_name + '''" WHERE ''' + conditions)

        rows = cur.fetchall()
        cur.close()
        return rows
