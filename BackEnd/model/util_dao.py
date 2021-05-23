import pymysql

class SelectNowDao:
    def select_now(self, connection):
        query = """
            SELECT now()
            """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)

            result = cursor.fetchone()
            now    = result["now()"]
            
            return now

