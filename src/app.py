from flask import Flask, request, Response
import json

from src.data_tables import data_tables

app = Flask(__name__)

tables = data_tables()
_host = "127.0.0.1"
_port = 5000


@app.route('/books', methods=['GET'])
def search():
    query_type = request.args.keys()
    try:
        if "isbn" in query_type:
            template = {"isbn": request.args.get("isbn").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif "title" in query_type:
            template = {"title": request.args.get("title").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif "subject" in query_type:
            template = {"category": request.args.get("subject").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/posts', methods=['POST'])
def create_new_post():
    try:
        body = json.loads(request.data)
        is_added = tables.add_listing(body)
        if is_added:
            rsp = Response('New post added', status=200, content_type='text/plain')
        else:
            #rsp
            pass
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/posts/<listing_id>', methods=['GET', 'PUT', 'DELETE'])
def post_by_id(listing_id):
    try:
        if request.method == 'PUT':
            body = json.loads(request.data)
            template = {'listing_id': listing_id}
            is_updated = tables.update_info("Listings", template, body)
            if is_updated:
                rsp = Response('Post updated', status=200, content_type='text/plain')
            else:
                rsp = Response("Update unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'listing_id': listing_id}
            is_deleted = tables.delete_info("Listings", template)
            if is_deleted:
                rsp = Response('Post deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == "GET":
            template = {'listing_id': listing_id}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users', methods=['POST'])
def create_user():
    try:
        body = json.loads(request.data)
        is_added = tables.add_user_info(body)
        if is_added:
            rsp = Response('New user added', status=200, content_type='text/plain')
        else:
            rsp = Response("Add unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/listings', methods=['GET'])
def get_user_posts(uni):
    try:
        template = {'uni': uni}
        res, is_success = tables.get_info("Listings", template)
        if is_success:
            rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>', methods=['GET', 'PUT'])
def user_by_uni(uni):
    try:
        if request.method == 'GET':
            template = {'uni': uni}
            res, is_success = tables.get_info("User_info", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == 'PUT':
            body = json.loads(request.data)
            template = {'uni': uni}
            is_updated = tables.update_info("User_info", template, body)
            if is_updated:
                rsp = Response('Post updated', status=200, content_type='text/plain')
            else:
                rsp = Response("Update unsuccessful", status=200, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/addresses', methods=['GET'])
def user_address(uni):
    try:
        template = {'uni': uni}
        res, is_success = tables.get_info("Addresses", template)
        if is_success:
            rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/orders', methods=['GET'])
def user_orders(uni):
    try:
        template = {'uni': uni}
        res, is_success = tables.get_info("Order_info", template)
        if is_success:
            rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/addresses', methods=['POST'])
def create_address():
    try:
        body = json.loads(request.data)
        is_added = tables.add_address(body)
        if is_added:
            rsp = Response('New address added', status=200, content_type='text/plain')
        else:
            rsp = Response("Add unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/addresses/<address_id>', methods=['PUT', 'DELETE'])
def address_by_id(address_id):
    try:
        if request.method == 'PUT':
            body = json.loads(request.data)
            template = {'address_id': address_id}
            is_updated = tables.update_info("Addresses", template, body)
            if is_updated:
                rsp = Response('Address updated', status=200, content_type='text/plain')
            else:
                rsp = Response("Update unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'address_id': address_id}
            is_deleted = tables.delete_info("Addresses", template)
            if is_deleted:
                rsp = Response('Address deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=200, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/orders', methods=['POST'])
def create_order():
    try:
        body = json.loads(request.data)
        is_added = tables.add_order_info(body)
        if is_added:
            rsp = Response('New order added', status=200, content_type='text/plain')
        else:
            rsp = Response("Add unsuccessful", status=200, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/orders/<order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(order_id):
    try:
        if request.method == 'PUT':
            body = json.loads(request.data)
            template = {'order_id': order_id}
            is_updated = tables.update_info("Order_info", template, body)
            if is_updated:
                rsp = Response('Order updated', status=200, content_type='text/plain')
            else:
                rsp = Response("Update unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'order_id': order_id}
            is_deleted = tables.delete_info("Order_info", template)
            if is_deleted:
                rsp = Response('Order deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=200, content_type='text/plain')
            return rsp
        elif request.method == "GET":
            template = {'order_id': order_id}
            res, is_success = tables.get_info("Order_info", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=200, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


if __name__ == '__main__':
    app.run(host=_host, port=_port)
