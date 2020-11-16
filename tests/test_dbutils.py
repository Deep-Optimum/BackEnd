from unittest import TestCase
import pymysql
import dbutils

class Test(TestCase):

    _default_connect_info = {
        'host': 'localhost',
        'user': 'root',
        'password': 'dbuser666',
        'db': 'sys',
        'port': 3306
    }
    _cnx = pymysql.connect(
        host=_default_connect_info['host'],
        user=_default_connect_info['user'],
        password=_default_connect_info['password'],
        db=_default_connect_info['db'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    def test_get_sql_from_file(self):
        path = "./schema.sql"
        result = dbutils.get_sql_from_file(path)
        self.assertEqual(len(result), 8)

    def test_get_sql_from_Non_exist_file(self):
        path = "./schemas.sql"
        result = dbutils.get_sql_from_file(path)
        self.assertEqual(result, None)

    def test_run_multiple_sql_statements(self):

        path = "./schema.sql"

        result = dbutils.get_sql_from_file(path)
        res, data = dbutils.run_multiple_sql_statements(result, conn=self._cnx, commit=True, fetch=True)
        print(res)

