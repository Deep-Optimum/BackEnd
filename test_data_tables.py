import unittest
from unittest import TestCase
import data_tables as dts
import pymysql
import json

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


class Testdata_tables(TestCase):


    def test_print_table(self):
        tables = dts.data_tables()
        print(tables)

    def test_get_key_cols(self):
        tables = dts.data_tables()
        key_cols = tables.get_key_cols()
        self.assertEqual(len(key_cols), 4)
        self.assertEqual(key_cols["User_info"], ['uni'])
        self.assertEqual(key_cols["Addresses"], ['address_id'])
        self.assertEqual(key_cols["Listings"], ['listing_id'])
        self.assertEqual(key_cols["Order_info"], ['order_id'])

    def test_get_table_class(self):
        tables = dts.data_tables()
        t = tables.get_table_class("User_info")
        self.assertIsNotNone(t)
        t = tables.get_table_class("Addresses")
        self.assertIsNotNone(t)
        t = tables.get_table_class("Listing")
        self.assertIsNotNone(t)
        t = tables.get_table_class("Order_info")
        self.assertIsNotNone(t)

    def test_create_and_close_session(self):
        tables = dts.data_tables()
        new_session = tables.create_session()
        self.assertIsNotNone(new_session)
        tables.commit_and_close_session(new_session)

    # @unittest.skip("Already deleted")
    # def test_delete_info(self):
    #
    #     table_name = "Order_info"
    #     template = None
    #     res = self.tables.delete_info(table_name, template)
    #     self.assertTrue(res)
    #     table_name = "Listings"
    #     template = None
    #     res = self.tables.delete_info(table_name, template)
    #     self.assertTrue(res)
    #     table_name = "Addresses"
    #     template = None
    #     res = self.tables.delete_info(table_name, template)
    #     self.assertTrue(res)
    #     table_name = "User_info"
    #     template = None
    #     res = self.tables.delete_info(table_name, template)
    #     self.assertTrue(res)

    # @unittest.skip("Already added")
    def test_add(self):
        tables = dts.data_tables()
        table_name = "Order_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Listings"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Addresses"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "User_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)

        new_user = {"uni": "sa1234",
                    "user_name": "King",
                    "email": "asd@columbia.edu",
                    "phone_number": "9212341234",
                    "credential": "king123"}

        is_success = tables.add_user_info(new_user)
        self.assertTrue(is_success)
        # Query
        table_name = "User_info"
        template = {"uni": "sa1234"}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["uni"], "sa1234")
        self.assertEqual(data[0]["user_name"], "King")
        self.assertEqual(data[0]["email"], "asd@columbia.edu")
        self.assertEqual(data[0]["phone_number"], "9212341234")
        self.assertEqual(data[0]["credential"], "king123")

        new_user = {"uni": "wl2750",
                    "user_name": "as",
                    "email": "aaaa@columbia.edu",
                    "phone_number": "1231231234",
                    "credential": "123123"}

        is_success = tables.add_user_info(new_user)
        self.assertTrue(is_success)
        # Query
        table_name = "User_info"
        template = {"uni": "wl2750"}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']
        self.assertEqual(data[0]["uni"], "wl2750")
        self.assertEqual(data[0]["user_name"], "as")
        self.assertEqual(data[0]["email"], "aaaa@columbia.edu")
        self.assertEqual(data[0]["phone_number"], "1231231234")
        self.assertEqual(data[0]["credential"], "123123")

        new_address = {"address_id": "4",
                       "uni": "wl2750",
                       "country": "USA",
                       "state": "NY",
                       "city": "NEW YORK",
                       "address": "102 ST ",
                       "zipcode": "12345"}

        is_success = tables.add_address(new_address)
        self.assertTrue(is_success)

        # Query
        table_name = "Addresses"
        template = {"address_id": 4}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        self.assertTrue(is_success)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["uni"], "wl2750")
        self.assertEqual(data[0]["country"], "USA")
        self.assertEqual(data[0]["address_id"], 4)


        new_listing = {"listing_id": 1,
                       "isbn": 123,
                       "uni": "sa1234",
                       "title": "Amen",
                       "category": "CS",
                       "price": 12.2,
                       "description": "A",
                       "image_url": "None",
                       "is_sold": 0}

        is_success = tables.add_listing(new_listing)
        self.assertTrue(is_success)

        # Query
        table_name = "Listings"
        template = {"listing_id": 1}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["uni"], "sa1234")
        self.assertEqual(data[0]["price"], 12.2)
        self.assertEqual(data[0]["is_sold"], 0)

        new_order = {"order_id": 1,
                       "isbn": 123,
                       "buyer_uni": "wl2750",
                       "seller_uni": "sa1234",
                       "listing_id": 1,
                       "transaction_amt": 12.2,
                       "status": "Completed"}

        is_success = tables.add_order_info(new_order)
        self.assertTrue(is_success)

        # Query
        table_name = "Order_info"
        template = {"order_id": 1}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        data = parsed['data']

        self.assertEqual(data[0]["buyer_uni"], "wl2750")
        self.assertEqual(data[0]["transaction_amt"], 12.2)
        self.assertEqual(data[0]["status"], "Completed")

        table_name = "Order_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Listings"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Addresses"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "User_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)

    # @unittest.skip("Already added")
    # def test_add_address(self):
    #
    #     new_address = {"address_id": "4",
    #                    "uni": "wl2750",
    #                    "country": "USA",
    #                    "state": "NY",
    #                    "city": "NEW YORK",
    #                    "address": "102 ST ",
    #                    "zipcode": "12345"}
    #
    #     is_success = T.add_address(new_address)
    #     self.assertTrue(is_success)
    #
    #     # Query
    #     table_name = "Addresses"
    #     template = {"address_id": 4}
    #     res, is_success= T.get_info(table_name=table_name, template=template)
    #     self.assertTrue(is_success)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #
    #     self.assertEqual(data[0]["uni"], "wl2750")
    #     self.assertEqual(data[0]["country"], "USA")
    #     self.assertEqual(data[0]["address_id"], 4)
    #
    # # @unittest.skip("Already added")
    # def test_add_listings(self):
    #     new_listing = {"listing_id": 1,
    #                    "isbn": 123,
    #                    "uni": "sa1234",
    #                    "title": "Amen",
    #                    "category": "CS",
    #                    "price": 12.2,
    #                    "description": "A",
    #                    "image_url": "None",
    #                    "is_sold": 0}
    #
    #     is_success = self.tables.add_listing(new_listing)
    #     self.assertTrue(is_success)
    #
    #     # Query
    #     table_name = "Listings"
    #     template = {"listing_id": 1}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #
    #     self.assertEqual(data[0]["uni"], "sa1234")
    #     self.assertEqual(data[0]["price"], 12.2)
    #     self.assertEqual(data[0]["is_sold"], 0)
    #
    # # @unittest.skip("Already added")
    # def test_add_order_info(self):
    #     new_order = {"order_id": 1,
    #                    "isbn": 123,
    #                    "buyer_uni": "wl2750",
    #                    "seller_uni": "sa1234",
    #                    "listing_id": 1,
    #                    "transaction_amt": 12.2,
    #                    "status": "Completed"}
    #
    #     is_success = self.tables.add_order_info(new_order)
    #     self.assertTrue(is_success)
    #
    #     # Query
    #     table_name = "Order_info"
    #     template = {"order_id": 1}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #
    #     self.assertEqual(data[0]["buyer_uni"], "wl2750")
    #     self.assertEqual(data[0]["transaction_amt"], 12.2)
    #     self.assertEqual(data[0]["status"], "Completed")
    # #
    # # # @unittest.skip("Already Done")
    # def test_get_info(self):
    #     print(self.tables)
    #     table_name = "User_info"
    #     template = {"uni": "sa1234"}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     self.assertTrue(is_success)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #     self.assertEqual(data[0]["uni"], "sa1234")
    #
    #     table_name = "Addresses"
    #     template = {"address_id": 4}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     self.assertTrue(is_success)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #     print(json.dumps(data, indent=4))
    #     self.assertEqual(data[0]["address_id"], 4)
    #
    #     table_name = "Listings"
    #     template = {"category": "CS"}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     self.assertTrue(is_success)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #     print(json.dumps(data, indent=4))
    #     self.assertEqual(data[0]["listing_id"], "1")
    #
    #     table_name = "Order_info"
    #     template = {"order_id": 1}
    #     res, is_success = self.tables.get_info(table_name=table_name, template=template)
    #     self.assertTrue(is_success)
    #     res = res.to_json(orient="table")
    #     parsed = json.loads(res)
    #     data = parsed['data']
    #     print(json.dumps(data, indent=4))
    #     self.assertEqual(data[0]["order_id"], "1")
    # @unittest.skip("Already Done")

    # @unittest.skip("Already Done")
    def test_get_info_empty_name(self):
        tables = dts.data_tables()
        table_name = ""
        template = {"uni": "sa1234"}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        self.assertFalse(is_success)
        self.assertIsNone(res)

        table_name = None
        template = {"uni": "sa1234"}
        res, is_success = tables.get_info(table_name=table_name, template=template)
        self.assertFalse(is_success)
        self.assertIsNone(res)

    # @unittest.skip("Already Done")
    def test_update_info(self):
        tables = dts.data_tables()
        table_name = "Order_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Listings"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "Addresses"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        table_name = "User_info"
        template = {}
        res = tables.delete_info(table_name, template)
        self.assertTrue(res)
        new_user = {"uni": "sa1234",
                    "user_name": "King",
                    "email": "asd@columbia.edu",
                    "phone_number": "9212341234",
                    "credential": "king123"}

        tables.add_user_info(new_user)

        new_user = {"uni": "wl2750",
                    "user_name": "as",
                    "email": "aaaa@columbia.edu",
                    "phone_number": "1231231234",
                    "credential": "123123"}

        tables.add_user_info(new_user)

        new_address = {"address_id": "4",
                       "uni": "wl2750",
                       "country": "USA",
                       "state": "NY",
                       "city": "NEW YORK",
                       "address": "102 ST ",
                       "zipcode": "12345"}
        tables.add_address(new_address)


        new_address = {"address_id": "4",
                       "uni": "wl2750",
                       "country": "USA",
                       "state": "NY",
                       "city": "NEW YORK",
                       "address": "102 ST ",
                       "zipcode": "12345"}

        is_success = tables.add_address(new_address)

        table_name = "Addresses"
        template = {"address_id": "4"}
        new_values = {"city": "NJ",
                      "zipcode": "12345"}
        is_success = tables.update_info(table_name=table_name, template=template,
                                new_values=new_values)
        self.assertTrue(is_success)
        # Query
        res, _ = tables.get_info(table_name=table_name, template=template)
        res = res.to_json(orient="table")
        parsed = json.loads(res)
        print(parsed['data'])
        data = parsed['data'][0]

        self.assertEqual(data['city'], "NJ")
        self.assertEqual(data['zipcode'], "12345")

    # @unittest.skip("Already Done")
    def test_update_info_empty_name(self):
        tables = dts.data_tables()

        table_name = ""
        template = {"uni": "sa1234"}
        new_values = {"emai": "NJ",
                      "zipcode": "12345"}
        is_success = tables.update_info(table_name, template, new_values)
        self.assertFalse(is_success)

        table_name = None
        template = {"uni": "sa1234"}
        new_values = {"emai": "NJ",
                      "zipcode": "12345"}
        is_success = tables.update_info(table_name, template, new_values)
        self.assertFalse(is_success)
    # @unittest.skip("Already Done")
    def test_get_row_count(self):
        tables = dts.data_tables()
        table_name = "Order_info"
        template = {}
        res = tables.delete_info(table_name, template)
        table_name = "Listings"
        template = {}
        res = tables.delete_info(table_name, template)
        table_name = "Addresses"
        template = {}
        res = tables.delete_info(table_name, template)
        table_name = "User_info"
        template = {}
        res = tables.delete_info(table_name, template)
        r = tables.get_row_count(tables._tables[0])  # User info
        self.assertEqual(r, 0)
        r = tables.get_row_count(tables._tables[1])  # Addresses
        self.assertEqual(r, 0)
        r = tables.get_row_count(tables._tables[2])  # listings
        self.assertEqual(r, 0)
        r = tables.get_row_count(tables._tables[3])  # order info
        self.assertEqual(r, 0)

    # @unittest.skip("Already deleted")
    def test_delete_info_2(self):

        tables = dts.data_tables()
        new_user = {"uni": "sa1234",
                    "user_name": "King",
                    "email": "asd@columbia.edu",
                    "phone_number": "9212341234",
                    "credential": "king123"}

        tables.add_user_info(new_user)

        new_user = {"uni": "wl2750",
                    "user_name": "as",
                    "email": "aaaa@columbia.edu",
                    "phone_number": "1231231234",
                    "credential": "123123"}

        tables.add_user_info(new_user)

        new_address = {"address_id": "4",
                       "uni": "wl2750",
                       "country": "USA",
                       "state": "NY",
                       "city": "NEW YORK",
                       "address": "102 ST ",
                       "zipcode": "12345"}
        tables.add_address(new_address)
        table_name = ""
        template = {"address_id": "4"}
        res = tables.delete_info(table_name=table_name, template=template)
        self.assertFalse(res)
        table_name = None
        template = {"address_id": "4"}
        res = tables.delete_info(table_name=table_name, template=template)
        self.assertFalse(res)

        table_name = "Addresses"
        template = {"address_id": "4"}
        res = tables.delete_info(table_name=table_name, template=template)
        self.assertTrue(res)

if __name__ == '__main__':

    t = Testdata_tables()
    t.test_create_and_close_session()
    t.test_delete_info()
    t.test_add_user_info()
    t.test_add_address()
    t.test_add_listings()
    t.test_add_order_info()
    t.test_get_key_cols()
    t.test_get_row_count()
    t.test_get_info()
    t.test_get_info_empty_name()
    t.test_print_table()
    t.test_update_info()
    t.test_update_info_empty_name()
    t.test_delete_info_2()


