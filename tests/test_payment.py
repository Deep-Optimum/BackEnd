import pytest
import json
from src import app
from dotenv import load_dotenv

extra_nonces = ["fake-valid-discover-nonce",
                "fake-valid-discover-nonce",
                "fake-valid-debit-nonce",
                "fake-valid-debit-nonce	"]

load_dotenv()


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client


def test_set_up():
    my_tables = app.tables

    list1 = ["User_info", "Addresses", "Listings", "Order_info"]
    for table_name in list1:
        filepath = "dummy_data/" + table_name + ".csv"
        res = my_tables.import_from_csv(table_name=table_name, filepath=filepath)
        assert res is True


def test_checkout_already_ordered(client):
    url = 'http://127.0.0.1:5000/checkouts/1'
    payload = {'payment_method_nonce': 'fake_valid_nonce'}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 201


def test_checkout_failed_both_confirm(client):
    url = 'http://127.0.0.1:5000/checkouts/2'
    payload = {'payment_method_nonce': 'fake_valid_nonce'}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 202


def test_checkout_success(client):
    url = 'http://127.0.0.1:5000/checkouts/3'
    payload = {'payment_method_nonce': 'fake-valid-discover-nonce'}
    # please note that nonces have 3 hour limit, even for fake ones.
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 200


def test_checkout_not_success(client):
    url = 'http://127.0.0.1:5000/checkouts/6'
    payload = {'payment_method_nonce': 'fake-consumed-nonce'}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 401


def test_checkout_not_id(client):
    url = 'http://127.0.0.1:5000/checkouts/11'
    payload = {'payment_method_nonce': 'fake_valid_nonce'}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 400


@pytest.fixture(scope="session", autouse=True)
def run_down():
    my_tables = app.tables
    list2 = ["Order_info", "Listings", "Addresses", "User_info"]
    for table_name in list2:
        my_tables.delete_info(table_name, template=None)
