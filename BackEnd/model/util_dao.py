import pymysql

<<<<<<< HEAD
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

=======

class UtilDao:

    def select_now(self, connection):
        query = "SELECT NOW() AS now"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result.get("now")
>>>>>>> f34f4d1 (commit)
