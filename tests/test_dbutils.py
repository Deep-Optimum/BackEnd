from unittest import TestCase
import pymysql
from utils import dbutils


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
    def test_get_connection(self):
        conn = dbutils.get_connection(self._default_connect_info)
        self.assertIsNotNone(conn)

    def test_get_sql_from_file(self):
        path = "../resources/schema.sql"
        result = dbutils.get_sql_from_file(path)
        self.assertEqual(len(result), 8)

    def test_get_sql_from_Non_exist_file(self):
        path = "./schemas.sql"
        result = dbutils.get_sql_from_file(path)
        self.assertEqual(result, None)

    def test_run_multiple_sql_statements(self):
        path = "../resources/schema.sql"
        result = dbutils.get_sql_from_file(path)
        res, data = dbutils.run_multiple_sql_statements(result, conn=self._cnx, commit=True, fetch=True)
        self.assertEqual(res, 0)

    def test_run_multiple_sql_statements_no_conn(self):

        path = "../resources/schema.sql"
        result = dbutils.get_sql_from_file(path)
        with self.assertRaises(ValueError) as context:
            dbutils.run_multiple_sql_statements(result, conn=None, commit=True, fetch=True)
        self.assertTrue("Connection cannot be None.", context)

    def test_run_multiple_sql_statements_no_statement(self):

        path = "../resources/schema.sql"
        result = dbutils.get_sql_from_file(path)
        with self.assertRaises(ValueError) as context:
            dbutils.run_multiple_sql_statements(None, conn=self._cnx, commit=True, fetch=True)
        self.assertTrue("Sql statement list is empty", context)

    def test_template_to_where_clause(self):
        template = {"address_id": "2", "uni": "wl2750"}
        actual = dbutils.template_to_where_clause(template)
        expected = (' WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
        self.assertEqual(actual, expected)

    def test_create_select(self):
        template = {"address_id": "2", "uni": "wl2750"}
        actual = dbutils.create_select("Addresses", template, is_select=True)
        expected = ('select  *  from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
        self.assertEqual(actual, expected)

    def test_create_select_w_field_list(self):
        template = {"address_id": "2", "uni": "wl2750"}
        fields = ["address_id", "state"]
        actual = dbutils.create_select("Addresses", template, fields=fields, is_select=True)
        expected = ('select  address_id,state  from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
        self.assertEqual(actual, expected)


    def test_create_delete(self):
        template = {"address_id": "2", "uni": "wl2750"}
        actual = dbutils.create_select("Addresses", template, is_select=False)
        expected = ('delete from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
        self.assertEqual(actual, expected)

    def test_create_update(self):
        template = {"uni": "wl2750"}
        changed_cols = {"email": "wl2750@columbia.edu"}
        actual = dbutils.create_update("User_info", template, changed_cols)
        expected = ('update User_info  set email=%s  WHERE  uni=%s ', ['wl2750@columbia.edu', 'wl2750'])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    t = Test()
    t.test_run_multiple_sql_statements_no_conn()
    t.test_run_multiple_sql_statements_no_statement()
    t.test_get_connection()
    t.test_create_delete()
    t.test_create_select()
    t.test_create_update()
    t.test_get_sql_from_file()
    t.test_run_multiple_sql_statements()
    t.test_get_sql_from_Non_exist_file()
    t.test_create_select_w_field_list()
    t.test_template_to_where_clause()

