from Data import Database

class DataAccess:
    def select(self, table_name, cols, parameters, values, operators):
        db = Database.Database()
        cur = db.connection.cursor()

        cols_str = "( "
        cols_size = len(cols)
        for i in range(0, cols_size):
            if i == cols_size - 1:
                cols_str += str(cols[i])
                break
            cols_str += (str(cols[i]) + ", ")
        cols_str += (" )")

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