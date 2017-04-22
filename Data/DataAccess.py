from Data import Database

class DataAccess:
    def select(self, table_name, cols, condition, value):
        conn = Database.Database()
        cur = conn.connection.cursor()
        if (condition == ""):
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''"''')
        else:
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''" WHERE ''' + condition + " = " + value)

        rows = cur.fetchall()
        cur.close()
        return rows

    # def select(self, table_name, cols, condition1, value1, condition2, value2):
    #     conn = Database.Database()
    #     cur = conn.connection.cursor()
    #     if (condition1 == ""):
    #         cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''"''')
    #     else:
    #         cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''" WHERE ''' + condition1 + " = " + value1 + " AND " + condition2 + " = " + value2)
    #
    #     rows = cur.fetchall()
    #     cur.close()
    #     return rows