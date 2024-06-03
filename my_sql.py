import sqlite3

my_SQL_name_file = '3.db'

class MySQL:
    def __init__(self):
        self.connect = sqlite3.connect(my_SQL_name_file, check_same_thread=False)

    def create_table(self, name, param):
        if not name or not param: return
        try:
            self.connect.execute(f"CREATE TABLE {name} ({param})")
            print(f"База данных {name} создана")
        except:
            pass

    def table_get(self, name, param, data):
        if not name: return None
        if not param or not data:
            return self.connect.execute(f"SELECT * FROM {name}").fetchall()
        else:
            cursor = self.connect.execute(f"SELECT * FROM {name} WHERE {param} = ?", (data,))
            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            return [{columns[i]: row[i] for i in range(len(columns))} for row in results]

    def table_get_all(self, name):
        cursor = self.connect.execute(f"SELECT * FROM {name}")
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        return [{columns[i]: row[i] for i in range(len(columns))} for row in results]

    def table_insert(self, name, param):
        if not name or not param: return
        len_param = '?, ' * int(len(param) - 1) + "?"
        self.connect.execute(f"INSERT INTO {name} VALUES (NULL, {len_param})", param)
        self.connect.commit()

    def table_update(self, name, player_id, field_name, new_value):
        print(player_id, field_name, new_value)
        query = f"UPDATE {name} SET {field_name} = ? WHERE player_id = ?"
        self.connect.execute(query, (new_value, player_id))
        self.connect.commit()

    def table_delete(self, name, param, table):
        if not name or not param: return
        self.connect.execute(f"DELETE FROM {name} WHERE {table} = {param}")
        self.connect.commit()


my_sql = MySQL()
