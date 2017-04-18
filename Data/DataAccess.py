from Data import Database

class DataAccess:

    def select(self, table_name, cols, condition, value):
        conn = Database.Database()
        cur = conn.connection.cursor()
        if (condition == ""):
            cur.execute("SELECT ( " + cols + " ) from " + table_name)
        else:
            cur.execute("SELECT ( " + cols + " ) from " + table_name + " WHERE " + condition + " = " + value)

        rows = cur.fetchall()
        conn.close()
        return rows