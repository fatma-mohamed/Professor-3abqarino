from Data import Database

class DataAccess:

    def selectGifsRandom(self, table_name, cols, parameters, values, operators):
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

    def test(self):
        sql = "SELECT COUNT(*) FROM "
        arr = ["Answers","Answers_Keywords","Gifs","Keywords","Notification","Questions_Answers","Synonyms","Tag","User"]
        db = Database.Database()
        cur = db.connection.cursor()
        for x in arr:
            cur.execute(sql + '"' + x + '"')
            print (x , ": " , cur.fetchall())

