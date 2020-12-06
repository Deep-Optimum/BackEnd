import pytest
import data_tables as dts
import json

@pytest.fixture(scope="module")
def my_tables():
    tables = dts.data_tables()
    return tables

def test_print_table(my_tables):
    print(my_tables)

def test_get_key_cols(my_tables):
    key_cols = my_tables.get_key_cols()
    assert len(key_cols), 4
    assert key_cols["User_info"] == ['uni']
    assert key_cols["Addresses"] == ['address_id']
    assert key_cols["Listings"] == ['listing_id']
    assert key_cols["Order_info"] == ['order_id']

def test_get_table_class(my_tables):
    t = my_tables.get_table_class("User_info")
    assert t is not None
    t = my_tables.get_table_class("Addresses")
    assert t is not None
    t = my_tables.get_table_class("Listing")
    assert t is not None
    t = my_tables.get_table_class("Order_info")
    assert t is not None

def test_create_and_close_session(my_tables):
    new_session = my_tables.create_session()
    assert new_session is not None
    my_tables.commit_and_close_session(new_session)

def test_delete_info(my_tables):

    table_name = "Order_info"
    template = None
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "Listings"
    template = None
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "Addresses"
    template = None
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "User_info"
    template = None
    res = my_tables.delete_info(table_name, template)
    assert res is True

def test_add_new_user(my_tables):

    table_name = "Order_info"
    template = {}
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "Listings"
    template = {}
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "Addresses"
    template = {}
    res = my_tables.delete_info(table_name, template)
    assert res is True
    table_name = "User_info"
    template = {}
    res = my_tables.delete_info(table_name, template)
    assert res is True

    new_user = {"uni": "sa1234",
                "user_name": "King",
                "email": "asd@columbia.edu",
                "phone_number": "9212341234",
                "credential": "king123"}

    is_success = my_tables.add_user_info(new_user)
    assert is_success is True

    new_user = {"uni": "wl2750",
                "user_name": "BL",
                "email": "wl2750@columbia.edu",
                "phone_number": "1231231234",
                "credential": "abe"}

    is_success = my_tables.add_user_info(new_user)
    assert is_success is True

def test_add_address(my_tables):

    new_address = {"address_id": "4",
                   "uni": "wl2750",
                   "country": "USA",
                   "state": "NY",
                   "city": "NEW YORK",
                   "address": "102 ST ",
                   "zipcode": "12345"}

    is_success = my_tables.add_address(new_address)
    assert is_success is True

def test_add_listings(my_tables):
    new_listing = {"listing_id": 1,
                   "isbn": 123,
                   "uni": "sa1234",
                   "title": "Amen",
                   "category": "CS",
                   "price": 12.2,
                   "description": "A",
                   "image_url": "None",
                   "is_sold": 0}

    is_success = my_tables.add_listing(new_listing)
    assert is_success is True

def test_add_new_order(my_tables):

    new_order = {"order_id": 1,
                   "isbn": 123,
                   "buyer_uni": "wl2750",
                   "seller_uni": "sa1234",
                   "listing_id": 1,
                   "transaction_amt": 12.2,
                   "status": "Completed",
                   'buyer_confirm': 0,
                   'seller_confirm': 0}

    is_success = my_tables.add_order_info(new_order)
    assert is_success is True

def test_get_info(my_tables):
    table_name = "User_info"
    template = {"uni": "sa1234"}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is True
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["uni"] == "sa1234"

    table_name = "Addresses"
    template = {"address_id": 4}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is True
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["address_id"] == 4

    table_name = "Listings"
    template = {"category": "CS"}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is True
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["listing_id"] == "1"

    table_name = "Order_info"
    template = {"order_id": 1}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is True
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["order_id"] == "1"

def test_get_info_empty_name(my_tables):
    table_name = ""
    template = {"uni": "sa1234"}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is False
    assert res is None

    table_name = None
    template = {"uni": "sa1234"}
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is False
    assert res is None

def test_get_info_similar(my_tables):
    table_name = "User_info"
    template = {"uni": "%2%"}
    res, is_success = my_tables.get_info(table_name=table_name, template=template, get_simillar=True)
    assert is_success is True

def test_update_user(my_tables):
    table_name = "User_info"
    template = {"uni": "wl2750"}
    new_values = {"phone_number": "999999999",
                  "credential": "11111"}
    is_success = my_tables.update_info(table_name=table_name, template=template,
                                    new_values=new_values)

    assert is_success is True

    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["uni"] == "wl2750"
    assert data[0]["phone_number"] == "999999999"
    assert data[0]["credential"] == "11111"

def test_update_address(my_tables):
    table_name = "Addresses"
    template = {"address_id": "4"}
    new_values = {"city": "NJ",
                  "zipcode": "12345"}
    is_success = my_tables.update_info(table_name=table_name, template=template,
                                    new_values=new_values)

    assert is_success is True
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["address_id"] == 4
    assert data[0]["city"] == "NJ"
    assert data[0]["zipcode"] == "12345"

def test_update_listing(my_tables):
    table_name = "Listings"
    template = {"listing_id": "1"}
    new_values = {"isbn": "123123",
                  "description": "abcd"}
    is_success = my_tables.update_info(table_name=table_name, template=template,
                                    new_values=new_values)

    assert is_success is True
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["listing_id"] == "1"
    assert data[0]["isbn"] == "123123"
    assert data[0]["description"] == "abcd"

def test_update_order(my_tables):
    table_name = "Order_info"
    template = {"order_id": "1"}
    new_values = {"status": "In Progress",
                  "buyer_confirm": "1"}
    is_success = my_tables.update_info(table_name=table_name, template=template,
                                    new_values=new_values)

    assert is_success is True
    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    res = res.to_json(orient="table")
    parsed = json.loads(res)
    data = parsed['data']
    assert data[0]["order_id"] == "1"
    assert data[0]["status"] == "In Progress"
    assert data[0]["buyer_confirm"] == 1

def test_update_info_empty_name(my_tables):

    table_name = ""
    template = {"uni": "sa1234"}
    new_values = {"emai": "NJ",
                  "zipcode": "12345"}
    is_success = my_tables.update_info(table_name, template, new_values)
    assert is_success is False

    table_name = None
    template = {"uni": "sa1234"}
    new_values = {"emai": "NJ",
                  "zipcode": "12345"}
    is_success = my_tables.update_info(table_name, template, new_values)
    assert is_success is False

def test_get_row_count(my_tables):

    r = my_tables.get_row_count(my_tables._tables[0])  # User info
    assert r == 2
    r = my_tables.get_row_count(my_tables._tables[1])  # Addresses
    assert r == 1
    r = my_tables.get_row_count(my_tables._tables[2])  # listings
    assert r == 1
    r = my_tables.get_row_count(my_tables._tables[3])  # order info
    assert r == 1

def test_delete_info_fail(my_tables):

    table_name = ""
    template = {"address_id": "4"}
    is_success = my_tables.delete_info(table_name=table_name, template=template)
    assert is_success is False
    table_name = None
    template = {"address_id": "4"}
    is_success = my_tables.delete_info(table_name=table_name, template=template)
    assert is_success is False

def test_delete_info(my_tables):
    table_name = "Addresses"
    template = {"address_id": "4"}
    is_success = my_tables.delete_info(table_name=table_name, template=template)
    assert is_success is True

    res, is_success = my_tables.get_info(table_name=table_name, template=template)
    assert is_success is True
    assert len(res) == 0