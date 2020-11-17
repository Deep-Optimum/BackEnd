from flask import Flask, request, Response
import json

from src.data_tables import data_tables

app = Flask(__name__)

tables = data_tables()


@app.route('/books', methods=['GET'])
def search():
    query_type = request.args.keys()
    try:
        if "isbn" in query_type:
            template = {"isbn": request.args.get("isbn")}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                pass
            return rsp
        elif "title" in query_type:
            template = {"title": request.args.get("title")}
            res, is_success= tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                pass
            return rsp
        elif "subject" in query_type:
            template = {"category": request.args.get("subject")}
            res, is_success = tables.get_info("Listings", template)
            if is_success:

                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                pass
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
            template = {listing_id: request.args.get(listing_id)}
            is_updated = tables.update_info("Listings", template, body)
            if is_updated:
                rsp = Response('Post updated', status=200, content_type='text/plain')
            else:
                #somethign else
                pass
            return rsp
        elif request.method == 'DELETE':

            return
        elif request.method == "GET":
            template = {listing_id: request.args.get(listing_id)}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                pass
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
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/listings', methods=['GET'])
def get_user_posts(uni):
    try:
        template = {uni: request.args.get(uni)}
        res, is_success = tables.get_info("Listings", template)
        if is_success:
            rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
        else:
            pass
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>', methods=['GET', 'PUT'])
def user_by_uni(uni):
    try:
        if request.method == 'GET':
            template = {uni: request.args.get(uni)}
            res, is_success = tables.get_info("User_info", template)
            if is_success:
                rsp = Response(res.to_json(orient="table"), status=200, content_type="application/json")
            else:
                pass
            return rsp
        elif request.method == 'PUT':
            body = json.loads(request.data)
            template = {uni: request.args.get(uni)}
            is_updated = tables.update_info("User_info", template, body)
            if is_updated:
                rsp = Response('Post updated', status=200, content_type='text/plain')
            else:
                pass
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/address', methods=['GET'])
def user_address(uni):
    return


@app.route('/users/<uni>/orders', methods=['GET'])
def user_orders(uni):
    return


@app.route('/addresses', methods=['POST'])
def create_address():
    return


@app.route('/addresses/<address_id>', methods=['PUT', 'DELETE'])
def address_by_id(address_id):
    return


@app.route('/orders', methods=['POST'])
def create_order():
    return


@app.route('/orders/<order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(order_id):
    return


if __name__ == '__main__':
    app.run()
