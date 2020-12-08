import pytest
import json
import app


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client


@pytest.mark.order(4)
def test_search(client):
    isbn_url = 'http://127.0.0.1:5000/books?isbn=9780072970548'
    rsp = client.get(isbn_url)
    assert rsp.status_code == 200
    data = json.loads(rsp.data)
    assert data[0]["isbn"] == '9780072970548'
    title_url = 'http://127.0.0.1:5000/books?title=introduction%20to%20algorithms'
    rsp = client.get(title_url)
    assert rsp.status_code == 200
    data = json.loads(rsp.data)
    assert data[0]["title"] == 'introduction to algorithms'


@pytest.mark.order(1)
def test_create_new_post(client):
    url = 'http://127.0.0.1:5000/posts'
    payload = {"listing_id": "1", "isbn": "9780072970548", "uni": "yz3781", "title": "introduction to algorithms",
               "price": 100.00, "category": "computer science", "description": "", "image_url": "", "is_sold": 0}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 200
    rsp = client.post(url, data=json.dumps(payload, indent=4))


@pytest.mark.order(10)
def test_post_by_id(client):
    url = 'http://127.0.0.1:5000/posts/1'
    payload = {"listing_id": "1", "isbn": "9780072970548", "uni": "yz3781", "title": "introduction to algorithms",
               "price": 110.00, "category": "computer science", "description": "", "image_url": "", "is_sold": 0}
    rsp_put = client.put(url, data=json.dumps(payload, indent=4))
    assert rsp_put.status_code == 200
    rsp_get = client.get(url)
    assert rsp_get.status_code == 200
    data = json.loads(rsp_get.data)
    assert data[0]["listing_id"] == '1'
    rsp_del = client.delete(url)
    assert rsp_del.status_code == 200


@pytest.mark.order(2)
def test_create_user(client):
    url = 'http://127.0.0.1:5000/users'
    payload = {"uni": "yz3781", "first_name": "D", "last_name": "Z", "user_name": "Dennis",
               "email": "yz3781@columbia.edu", "phone_number": "", "credential": ""}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    payload = {"uni": "ab1234", "first_name": "A", "last_name": "B", "user_name": "Abby",
               "email": "ab1234@columbia.edu", "phone_number": "", "credential": ""}
    rsp = client.post(url, data=json.dumps(payload, indent=4))


@pytest.mark.order(5)
def test_get_user_posts(client):
    url = 'http://127.0.0.1:5000/users/yz3781/listings'
    rsp = client.get(url)
    assert rsp.status_code == 200
    data = json.loads(rsp.data)
    assert data[0]["uni"] == 'yz3781'


def test_user_by_uni(client):
    url = 'http://127.0.0.1:5000/users/yz3781'
    payload = {"uni": "yz3781", "user_name": "Dennis", "email": "yz3710@columbia.edu",
               "phone_number": "1112223344", "credential": ""}
    rsp_put = client.put(url, data=json.dumps(payload, indent=4))
    assert rsp_put.status_code == 200
    rsp_get = client.get(url)
    assert rsp_get.status_code == 200
    data = json.loads(rsp_get.data)
    assert data[0]["uni"] == 'yz3781'


@pytest.mark.order(6)
def test_user_address(client):
    url = 'http://127.0.0.1:5000/users/yz3781/addresses'
    rsp = client.get(url)
    assert rsp.status_code == 200
    data = json.loads(rsp.data)
    assert data[0]["uni"] == 'yz3781'


@pytest.mark.order(7)
def test_user_orders(client):
    url = 'http://127.0.0.1:5000/users/yz3781/orders'
    rsp = client.get(url)
    assert rsp.status_code == 200
    data = json.loads(rsp.data)
    assert data[0]["buyer_uni"] == 'yz3781'


@pytest.mark.order(3)
def test_create_address(client):
    url = 'http://127.0.0.1:5000/addresses'
    payload = {"address_id": "1", "uni": "yz3781", "country": "United States", "state": "NY", "city": "New York",
               "address": "xx", "zipcode": "10025"}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 200
    rsp = client.post(url, data=json.dumps(payload, indent=4))


def test_address_by_id(client):
    url = 'http://127.0.0.1:5000/addresses/1'
    payload = {"address_id": "1", "uni": "yz3781", "country": "United States", "state": "NY", "city": "New York",
               "address": "xx street", "zipcode": "10025"}
    rsp_put = client.put(url, data=json.dumps(payload, indent=4))
    assert rsp_put.status_code == 200
    rsp_del = client.delete(url)
    assert rsp_del.status_code == 200


@pytest.mark.order(4)
def test_create_order(client):
    url = 'http://127.0.0.1:5000/orders'
    payload = {"order_id": "1", "buyer_uni": "yz3781", "seller_uni": "ab1234", "listing_id": "1",
               "transaction_amt": 78.00, "status": "In progress", "buyer_confirm": 0, "seller_confirm": 1}
    rsp = client.post(url, data=json.dumps(payload, indent=4))
    assert rsp.status_code == 200
    rsp = client.post(url, data=json.dumps(payload, indent=4))


@pytest.mark.order(9)
def test_order_by_id(client):
    url = 'http://127.0.0.1:5000/orders/1'
    payload = {"order_id": "1", "buyer_uni": "yz3781", "seller_uni": "ab1234", "listing_id": "1",
               "transaction_amt": 78.00, "status": "Completed","buyer_confirm": 0, "seller_confirm": 1}
    rsp_put = client.put(url, data=json.dumps(payload, indent=4))
    assert rsp_put.status_code == 200
    rsp_get = client.get(url)
    assert rsp_get.status_code == 200
    data = json.loads(rsp_get.data)
    assert data[0]["order_id"] == '1'
    rsp_del = client.delete(url)
    assert rsp_del.status_code == 200


@pytest.mark.order(8)
def test_confirm_order(client):
    url = 'http://127.0.0.1:5000/orders/1/yz3781'
    rsp = client.put(url)
    assert rsp.status_code == 200
