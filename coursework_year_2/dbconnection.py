import jaydebeapi


class Connection():
    def __init__(self):
        self.conn = jaydebeapi.connect("com.microsoft.sqlserver.jdbc.SQLServerDriver",
                                       "jdbc:sqlserver://;serverName=localhost;databaseName=master",
                                       ["sa", "yourStrong(!)Password"],
                                       "mssql-jdbc-9.2.1.jre8.jar")

    def select_all_from(self, table):
        curs = self.conn.cursor()
        curs.execute("use [library];")
        select = f"SELECT * from {table};"
        curs.execute(select)
        records = curs.fetchall()
        curs.close()
        return records

    def insert_into(self, table: str, values):
        curs = self.conn.cursor()
        curs.execute("use [library];")
        insert = f"INSERT INTO {table} VALUES {values};"
        curs.execute(insert)
        curs.close()

    def execute_statement(self, statement: str, returning: bool):
        curs = self.conn.cursor()
        curs.execute("use [library];")
        curs.execute(statement)
        if not returning:
            curs.close()
        else:
            rows = curs.fetchall()
            curs.close()
            return rows

    def choose_table_columns(self, table: str, columns: list):
        curs = self.conn.cursor()
        curs.execute("use [library];")
        select = "select "
        for el in columns:
            if el != columns[-1]:
                select += el + ", "
            else:
                select += el + " "
        select += f"from {table};"
        curs.execute(select)
        rows = curs.fetchall()
        curs.close()
        return rows

    # def find_column_bycondition(self, table: str, ocolumn: str, incolumn: str, value, valuetype: str):
    #     valuetype = valuetype.lower()
    #     curs = self.conn.cursor()
    #     curs.execute("use [library];")
    #     if valuetype == 'varchar' or valuetype == 'date' or valuetype == 'datetime':
    #         select = f"select {ocolumn} from {table} where LOWER({incolumn}) = LOWER('{value}');"
    #         # print(select)
    #     elif valuetype == 'int' or valuetype == 'binary' or valuetype == 'float':
    #         select = f"select {ocolumn} from {table} where {incolumn} = {value};"
    #     curs.execute(select)
    #     rows = curs.fetchall()
    #     if len(rows) == 0:
    #         curs.close()
    #         return False
    #     else:
    #         curs.close()
    #         return rows[0][0]

    def find_column_by_conditions(self, table: str, ocolumn: str, incolumns: list, values: list, valuetypes: list):
        valuetypes = [valuetype.lower() for valuetype in valuetypes]
        curs = self.conn.cursor()
        curs.execute("use [library];")
        select = f"select {ocolumn} from {table} where "
        for i in range(len(incolumns)):
            if valuetypes[i] == 'int':
                select += f"{incolumns[i]} = {values[i]} and "
            else:
                select += f"{incolumns[i]} = '{values[i]}' and "
        curs.execute(select[:-5])
        rows = curs.fetchall()
        curs.close()
        if len(rows) == 0:
            return False
        else:
            return rows[0][0]

    # def check_worker(self, ssn, inn, passport):
    #     curs = self.conn.cursor()
    #     curs.execute("use [library];")
    #     select = f"select dbo.check_worker('{ssn}', '{inn}', '{passport}')"
    #     curs.execute(select)
    #     rows = curs.fetchall()
    #     if rows[0][0]:
    #         return False
    #     else:
    #         return True


# conn = Connection()
# curs = conn.conn.cursor()
# curs.execute("use [library];")
# conn.find_column_bycondition('Status', 'StatusID', 'Name', 'allowed', 'varchar')
# print(conn.find_column_by_conditions('Author', 'AuthorID', ['FirstName', 'LastName'],
#                                      ['Ivan', 'Ivanov'], ['str', 'str']))
# curs.execute("select LibraryID from Library where Name = 'Dostoevskogo library';")
# records = curs.fetchall()
# print(records)
