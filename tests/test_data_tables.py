from unittest import TestCase
from src import data_tables as dts
import pymysql
import json


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
    tables = dts.data_tables()

    def test_print_table(self):
        print(self.tables)

    def test_get_info(self):
        tables = dts.data_tables()
        table = tables.get_table("user_info")
        res = tables.get_info(table)
        print(res)

        def test_add_user_info(self):
            tables = dts.data_tables()
            User_info = tables.get_table("user_info")

            new_user = {"uni": "wl2777",
                        "user_name": "ABC123",
                        "email": "wl2777@columbia.edu",
                        "phone_number": "7021231234",
                        "credential": "123123"}
            tables.add_user_info(new_user)
            res = tables.get_info(User_info)
            print(res)

    def test_get_key_cols(self):
        key_cols = self.tables.get_key_cols()
        self.assertEqual(len(key_cols), 4)
        self.assertEqual(key_cols["User_info"], ['uni'])
        self.assertEqual(key_cols["Addresses"], ['address_id'])
        self.assertEqual(key_cols["Listings"], ['listing_id', 'isbn'])
        self.assertEqual(key_cols["Order_info"], ['order_id'])

    def test_create_and_close_session(self):
        new_session = self.tables.create_session()
        self.assertIsNotNone(new_session)
        self.tables.commit_and_close_session(new_session)

    def test_get_row_count(self):
        r = self.tables.get_row_count(self.tables._tables[0])  # User info
        self.assertEqual(r, 3)
        r = self.tables.get_row_count(self.tables._tables[1])  # Addresses
        self.assertEqual(r, 2)
        r = self.tables.get_row_count(self.tables._tables[2])  # listings
        self.assertEqual(r, 2)
        r = self.tables.get_row_count(self.tables._tables[3])  # order info
        self.assertEqual(r, 1)

    def test_get_info(self):
        table_name = "User_info"
        template = {"uni": "wl2750"}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        self.assertEqual(data[0]["uni"], "wl2750")

        table_name = "Addresses"
        template = {"address_id": "2"}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        print(json.dumps(data, indent=4))
        self.assertEqual(data[0]["address_id"], 2)

        table_name = "Listings"
        template = {"listing_id": "2"}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        print(json.dumps(data, indent=4))
        self.assertEqual(data[0]["listing_id"], "2")

        table_name = "Order_info"
        template = {"order_id": "1"}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        print(json.dumps(data, indent=4))
        self.assertEqual(data[0]["order_id"], "1")

    def test_update_info(self):
        print("Start")
        table_name = "Addresses"
        template = {"address_id": "1"}
        new_values = {"city": "NJ",
                      "zipcode": "12345"}
        res = self.tables.update_info(table_name=table_name, template=template,
                                new_values=new_values)
        if res:
            print("ok")
        # Query
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        print(data)



    def test_add_user_info(self):
        new_user = {"uni": "sa1234",
                    "user_name": "King",
                    "email": "asd@columbia.edu",
                    "phone_number": "9212341234",
                    "credential": "king123"}

        self.tables.add_user_info(new_user)

        # Query
        table_name = "User_info"
        template = {"uni": "sa1234"}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["uni"], "sa1234")
        self.assertEqual(data[0]["user_name"], "King")
        self.assertEqual(data[0]["email"], "asd@columbia.edu")
        self.assertEqual(data[0]["phone_number"], "9212341234")
        self.assertEqual(data[0]["credential"], "king123")

    def test_add_address(self):
        new_address = {"address_id": "4",
                       "uni": "sa1234",
                       "country": "USA",
                       "state": "NY",
                       "city": "NEW YORK",
                       "address": "102 ST ",
                       "zipcode": "12345"}

        self.tables.add_address(new_address)

        # Query
        table_name = "Addresses"
        template = {"address_id": 4}
        res = self.tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["uni"], "sa1234")
        self.assertEqual(data[0]["country"], "USA")
        self.assertEqual(data[0]["address_id"], 4)


    def test_delete_info(self):
        table_name = "Addresses"
        template = {"address_id": "4"}
        res = self.tables.delete_info(table_name=table_name, template=template)
        if res:
            res = res.to_json(orient="table")
            parsed = json.loads(res)
            data = parsed['data']
            print(json.dumps(data, indent=4))
            self.assertEqual(data[0]["address_id"], 2)
        print("ok")
