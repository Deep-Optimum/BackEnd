import unittest
import json
import requests


class TestApp(unittest.TestCase):
    def test_search(self):
        isbn_url = 'http://127.0.0.1:5000/books?isbn=9780072970548'
        rsp = requests.get(isbn_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["isbn"], '9780072970548')
        title_url = 'http://127.0.0.1:5000/books?title=introduction%20to%20algorithms'
        rsp = requests.get(title_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["title"], 'introduction to algorithms')
        subject_url = 'http://127.0.0.1:5000/books?subject=computer%20science'
        rsp = requests.get(title_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["subject"], 'computer science')

    def test_create_new_post(self):
        url = 'http://127.0.0.1:5000/posts'
        payload = {'listing_id': '1', 'isbn': '9780072970548', 'uni': 'yz3781', 'title': 'introduction to algorithms',
                   'price': 100.00, 'category': 'computer science', 'description': "", 'image_url': "", 'is_sold': 0}
        rsp = requests.post(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()['url'], url)

    def test_post_by_id(self):
        url = 'http://127.0.0.1:5000/posts/1'
        rsp_get = requests.get(url)
        self.assertEqual(rsp_get.status_code, 200)
        self.assertEqual(rsp_get.json()["listing_id"], '1')
        payload = {'listing_id': '1', 'isbn': '9780072970548', 'uni': 'yz3781', 'title': 'introduction to algorithms',
                   'price': 110.00, 'category': 'computer science', 'description': "", 'image_url': "", 'is_sold': 0}
        rsp_put = requests.put(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp_put.status_code, 200)
        self.assertEqual(rsp_put.json()["url"], url)
        rsp_del = requests.delete(url)
        self.assertEqual(rsp_del.status_code, 200)
        self.assertEqual(rsp_del.json()["url"], url)

    def test_create_users(self):
        url = 'http://127.0.0.1:5000/users'
        payload = {'uni': 'yz3781', 'user_name': 'Dennis', 'email': 'yz3781@columbia.edu',
                   'phone_number': "", 'credential': ""}
        rsp = requests.post(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()['url'], url)

    def test_get_user_posts(self):
        url = 'http://127.0.0.1:5000/users/yz3781/listings'
        rsp = requests.get(url)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["uni"], 'yz3781')

    def test_user_by_uni(self):
        url = 'http://127.0.0.1:5000/users/yz3781'
        rsp_get = requests.get(url)
        self.assertEqual(rsp_get.status_code, 200)
        self.assertEqual(rsp_get.json()["uni"], 'yz3781')
        payload = {'uni': 'yz3781', 'user_name': 'Dennis', 'email': 'yz3781@columbia.edu',
                   'phone_number': '1112223344', 'credential': ""}
        rsp_put = requests.put(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp_put.status_code, 200)
        self.assertEqual(rsp_put.json()["url"], url)

    def test_user_address(self):
        url = 'http://127.0.0.1:5000/users/yz3781/addresses'
        rsp_get = requests.get(url)
        self.assertEqual(rsp_get.status_code, 200)
        self.assertEqual(rsp_get.json()["uni"], 'yz3781')

    def test_user_orders(self):
        url = 'http://127.0.0.1:5000/users/yz3781/orders'
        rsp_get = requests.get(url)
        self.assertEqual(rsp_get.status_code, 200)
        self.assertEqual(rsp_get.json()["uni"], 'yz3781')

    def test_create_address(self):
        url = 'http://127.0.0.1:5000/addresses'
        payload = {'address_id': '1', 'uni': 'yz3781', 'country': 'United States', 'state': 'NY', 'city': 'New York',
                   'address': 'xx', 'zipcode': '10025'}
        rsp = requests.post(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["url"], url)

    def test_address_by_id(self):
        url = 'http://127.0.0.1:5000/addresses/1'
        rsp_del = requests.delete(url)
        self.assertEqual(rsp_del.status_code, 200)
        self.assertEqual(rsp_del.json()["url"], url)
        payload = {'address_id': '1', 'uni': 'yz3781', 'country': 'United States', 'state': 'NY', 'city': 'New York',
                   'address': 'xx street', 'zipcode': '10025'}
        rsp_put = requests.put(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp_put.status_code, 200)
        self.assertEqual(rsp_put.json()["url"], url)

    def test_create_order(self):
        url = 'http://127.0.0.1:5000/orders'
        payload = {'order_id': '1', 'buyer_uni': 'yz3781', 'seller_uni': 'ab1234', 'listing_id': '2',
                   'transaction_amt': 78.00, 'status': 'In progress'}
        rsp = requests.post(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()["url"], url)

    def test_order_by_id(self):
        url = 'http://127.0.0.1:5000/orders/1'
        rsp_get = requests.get(url)
        self.assertEqual(rsp_get.status_code, 200)
        self.assertEqual(rsp_get.json()["order_id"], '1')
        payload = {'order_id': '1', 'buyer_uni': 'yz3781', 'seller_uni': 'ab1234', 'listing_id': '2',
                   'transaction_amt': 78.00, 'status': 'Completed'}
        rsp_del = requests.delete(url)
        self.assertEqual(rsp_del.status_code, 200)
        self.assertEqual(rsp_del.json()["url"], url)
        rsp_put = requests.put(url, data=json.dumps(payload, indent=4))
        self.assertEqual(rsp_put.status_code, 200)
        self.assertEqual(rsp_put.json()["url"], url)


if __name__ == '__main__':
    unittest.main()
