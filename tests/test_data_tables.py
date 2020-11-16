from unittest import TestCase
import data_tables as dts
import pymysql


class Testdata_tables(TestCase):
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

    def test_creation(self):
        tables = dts.data_tables()
        tables.print_tables()


class Testdata_tables(TestCase):
    def test_get_info(self):
        tables = dts.data_tables()
        table = tables.get_table("user_info")
        res = tables.get_info(table)
        print(res)


class Testdata_tables(TestCase):
    def test_add_user_info(self):
        tables = dts.data_tables()
        User_info = tables.get_table("user_info")

        new_user= {"uni": "wl2777",
                    "user_name":"ABC123",
                    "email":"wl2777@columbia.edu",
                    "phone_number":"7021231234",
                    "credential":"123123"}
        tables.add_user_info(new_user)
        res = tables.get_info(User_info)
        print(res)