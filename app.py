from flask import Flask, request, Response, redirect, url_for, flash, render_template
import json
from dotenv import load_dotenv
import braintree
from payment import generate_client_token, transact, find_transaction

from data_tables import data_tables

load_dotenv()

app = Flask(__name__)

tables = data_tables()
_host = "127.0.0.1"
_port = 5000

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
                rsp = Response(json.dumps(data, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif "title" in request.args:
            template = {"title": request.args.get("title").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
        elif "subject" in request.args:
            template = {"category": request.args.get("subject").lower()}
            res, is_success = tables.get_info("Listings", template)
            if is_success:
                data = json.loads(res.to_json(orient="table"))["data"]
                rsp = Response(json.dumps(data, default=str), status=200, content_type="application/json")
            else:
                rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
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
            data = json.loads(res.to_json(orient="table"))["data"]
            print("data", data)
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
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
            data = json.loads(res.to_json(orient="table"))["data"]
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
        return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


@app.route('/users/<uni>/orders', methods=['GET'])
def user_orders(uni):
    try:
        template = {'buyer_uni': uni}
        res, is_success = tables.get_info("Order_info", template)
        if is_success:
            data = json.loads(res.to_json(orient="table"))["data"]
            rsp = Response(json.dumps(data), status=200, content_type="application/json")
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
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
            rsp = Response("Add unsuccessful", status=400, content_type='text/plain')
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
    except Exception as e:
        print(e)
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
                is_updated = tables.update_info("Order_info", template, {"buyer_confirm": 1})
                if is_updated:
                    rsp = Response("Buyer confirmed", status=200, content_type='text/plain')
                    return rsp
        else:
            rsp = Response("Query unsuccessful", status=400, content_type='text/plain')
            return rsp
    except Exception as e:
        print(e)
        rsp = Response("Internal error", status=500, content_type='text/plain')
        return rsp


# Checkouts
#@app.route('/checkouts/new', methods=['GET'])
#def new_checkout():
#    client_token = generate_client_token()
#    return client_token
#    #return render_template('checkouts/new.html', client_token=client_token)

@app.route("/checkouts/<order_id>", methods=['POST'])
def create_checkout(order_id):
    #body = json.loads(request.data)
    template = {'order_id': order_id}
    res, is_success = tables.get_info("Order_info", template)
    if is_success:
        # Order Id in the DB - proceed with transaction
        amount = float(res["transaction_amt"])
        result = transact({
            'amount': amount,
            'payment_method_nonce': request.form["payment_method_nonce"],
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success or result.transaction:
            tables.get_info()
            return Response("Transaction success", status=200, content_type="text/plain")
            #return redirect(url_for("show_checkout", transaction_id=result.transaction.id))
        else:
            for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
            return Response("Transaction failed", status=201, content_type="text/plain")
            #return redirect(url_for('new_checkout'))
    else:
        return Response('Query failed', status=200, content_type='text/plain')


@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your transaction has been successfully processed. Please coordinate a time with your seller.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. Try again.'
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)


if __name__ == '__main__':
    app.debug = True
    app.run(host=_host, port=_port)