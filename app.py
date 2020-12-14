"""
    Defines all the endpoints.
"""
import json
import os
from flask import Flask, request, Response, flash
from dotenv import load_dotenv
import braintree
from flask_cors import CORS
from payment import transact, find_transaction, generate_client_token # pylint: disable=no-name-in-module, unused-import
import data_tables # pylint: disable=import-error, invalid-name
import send_email # pylint: disable=import-error
load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get('SECRET_KEY')

tables = data_tables.data_tables()
_HOST = "127.0.0.1"
_PORT = 5000
# pylint: disable=missing-function-docstring, broad-except, inconsistent-return-statements, no-else-return, unused-variable
TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


@app.route('/books', methods=['GET'])
def search():
    try:
        if "isbn" in request.args:
            template = {"isbn": request.args.get("isbn").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif "title" in request.args:
            word_list = request.args.get("title").lower().split()
            query_str = '%'+'%'.join(word_list)+'%'
            template = {"title": query_str}
            res, is_success = tables.get_info("Listings", template, get_similar=True,
                                              order_by=['category'], is_or=True)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data, default=str), status=200,
                               content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
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
                res, _ = tables.get_info("Listings", template)
                data = json.loads(res.to_json(orient="table"))["data"]
                price = data[0]["price"]
                tables.update_info("Order_info", template, {"transaction_amt": price})
            else:
                rsp = Response("Update unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'listing_id': listing_id}
            is_deleted = tables.delete_info("Listings", template)
            if is_deleted:
                rsp = Response('Post deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == "GET":
            template = {'listing_id': listing_id}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/listings', methods=['GET'])
def get_user_posts(uni):
    try:
        template = {'uni': uni}
        res, is_success = tables.get_info("Listings", template)
        if is_success:
            data = json.loads(res.to_json(orient="table"))["data"]
            for i in data:
                listing_id = i["listing_id"]
                res_get, success = tables.get_info("Order_info", {'listing_id': listing_id})
                order_data = json.loads(res_get.to_json(orient="table"))['data']
                if len(order_data) != 0:
                    i.update(order_data[0])
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>', methods=['GET', 'PUT'])
def user_by_uni(uni):
    try:
        if request.method == 'GET':
            template = {'uni': uni}
            res, is_success = tables.get_info("User_info", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == 'PUT':
            body = json.loads(request.data)
            template = {'uni': uni}
            is_updated = tables.update_info("User_info", template, body)
            if is_updated:
                rsp = Response('Post updated', status=200, content_type='text/plain')
            else:
                rsp = Response("Update unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/addresses', methods=['GET'])
def user_address(uni):
    try:
        template = {'uni': uni}
        res, is_success = tables.get_info("Addresses", template)
        if is_success:
            data = json.loads(res.to_json(orient="table"))["data"]
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/orders', methods=['GET'])
def user_orders(uni):
    try:
        template = {'buyer_uni': uni}
        res, is_success = tables.get_info("Order_info", template)
        if is_success:
            data = json.loads(res.to_json(orient="table"))["data"]
            for i in data:
                listing_id = i["listing_id"]
                res_get, success = tables.get_info("Listings", {'listing_id': listing_id})
                listing_data = json.loads(res_get.to_json(orient="table"))['data'][0]
                i.update(listing_data)
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
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
                rsp = Response("Update unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'address_id': address_id}
            is_deleted = tables.delete_info("Addresses", template)
            if is_deleted:
                rsp = Response('Address deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/orders', methods=['POST'])
def create_order():
    try:
        body = json.loads(request.data)
        listing_id = body["listing_id"]
        template = {"listing_id": listing_id}
        tables.update_info("Listings", template, {"is_sold": 1})
        is_added = tables.add_order_info(body)
        if is_added:
            rsp = Response('New order added', status=200, content_type='text/plain')
            send_email.send_email(body)
        else:
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as exp:
        print(exp)
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
                rsp = Response("Update unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == 'DELETE':
            template = {'order_id': order_id}
            is_deleted = tables.delete_info("Order_info", template)
            if is_deleted:
                rsp = Response('Order deleted', status=200, content_type='text/plain')
            else:
                rsp = Response("Delete unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif request.method == "GET":
            template = {'order_id': order_id}
            res, is_success = tables.get_info("Order_info", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/orders/<order_id>/<uni>', methods=['PUT'])
def confirm_order(order_id, uni):
    try:
        template = {'order_id': order_id}
        res, is_success = tables.get_info("Order_info", template)
        if is_success:
            data = json.loads(res.to_json(orient="table"))["data"]
            buyer_uni = data[0]['buyer_uni']
            if buyer_uni == uni:
                is_updated = tables.update_info("Order_info", template,
                                {"buyer_confirm": 1, 'status': 'Completed'})
                if is_updated:
                    tables.update_info("Listing", template, {'is_sold': 1})
                    send_email.send_email(data[0])
                    rsp = Response("Buyer confirmed", status=200, content_type='text/plain')
                    return rsp
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as exp:
        print(exp)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route("/checkouts/<order_id>", methods=['POST'])
def create_checkout(order_id):
    template = {'order_id': order_id}
    res, is_success = tables.get_info("Order_info", template)
    body = json.loads(request.data)
    if len(res) != 0:
        # check the following:
        # 1. Both buyer and seller must have confirmed
        buyer_confirm = int(res["buyer_confirm"][0])
        seller_confirm = int(res["seller_confirm"][0])
        if buyer_confirm == 0 or seller_confirm == 0:
            return Response("Both buyer and seller must confirm", status=202,
                            content_type="text/plain")
        # 2. Status is In Progress
        status = str(res["status"][0])
        if status == "In Progress":
            # Order Id in the DB - proceed with transaction
            amount = str(float(res["transaction_amt"]))
            result = transact({
                'amount': amount,
                'payment_method_nonce': body["payment_method_nonce"],
                'options': {
                    'submit_for_settlement': True
                }
            })
            if result.is_success or result.transaction:
                tables.update_info("Order_info", template, {'status': 'Completed'})
                tables.update_info("Listing", template, {'is_sold': 1})
                return Response("Transaction success", status=200, content_type="text/plain")
            else:
                for err in result.errors.deep_errors:
                    flash('Error: %s: %s' % (err.code, err.message))
                return Response("Transaction failed", status=401, content_type="text/plain")

        else:
            return Response("Error. Please check with the admin.", status=201,
                            content_type="text/plain")
    else:
        return Response('Query failed', status=400, content_type='text/plain')

@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    token = {"client_token": client_token}
    rsp = Response(json.dumps(token, indent=4), status=200, content_type="application/json")
    return rsp

# @app.route('/checkouts/<transaction_id>', methods=['GET'])
# def show_checkout(transaction_id):
#     transaction = find_transaction(transaction_id)
#     result = {}
#     if transaction.status in TRANSACTION_SUCCESS_STATUSES:
#         result = {
#             'header': 'Sweet Success!',
#             'icon': 'success',
#             'message': 'Your transaction has been successfully processed. Please
#             coordinate a time with your seller.'
#         }
#     else:
#         result = {
#             'header': 'Transaction Failed',
#             'icon': 'fail',
#             'message': 'Your test transaction has a status of ' +
#             transaction.status + '. Try again.'
#         }
#     return Response(json.dumps(result), status=200, content_type='text/plain')
#     #return render_template('checkouts/show.html', transaction=transaction, result=result)


if __name__ == '__main__':
    app.debug = True
    app.run(host=_HOST, port=_PORT)
