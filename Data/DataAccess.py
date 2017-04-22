from Data import Database

class DataAccess:

    def select(self, table_name, cols, condition):
        conn = Database.Database()
        cur = conn.connection.cursor()
        if (condition == ""):
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''"''')
        else:
            cur.execute("SELECT ( " + cols + ''' ) from "''' + table_name + '''" WHERE ''' + condition )

        rows = cur.fetchall()
        cur.close()
        return rows