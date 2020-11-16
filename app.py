from flask import Flask, request, Response
from datetime import datetime
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/books', methods=['GET'])
def search():
    return


@app.route('/posts', methods=['POST'])
def create_new_post():
    return


@app.route('/posts/<postid>', methods=['PUT', 'DELETE'])
def post_by_id(postid):
    return


@app.route('/users', methods=['POST'])
def create_user():
    return


@app.route('/users/<uni>/posts', methods=['GET'])
def get_user_posts(uni):
    return


@app.route('/users/<uni>', methods=['GET', 'PUT'])
def user_by_uni(uni):
    return


@app.route('/users/<uni>/addresses', methods=['GET'])
def user_address(uni):
    return


@app.route('/users/<uni>/orders', methods=['GET'])
def user_orders(uni):
    return


@app.route('/addresses', methods=['POST'])
def create_address():
    return


@app.route('/addresses/<addressid>', methods=['PUT', 'DELETE'])
def address_by_id(addressid):
    return


@app.route('/orders', methods=['POST'])
def create_order():
    return


@app.route('/orders/<orderid>', methods=['PUT', 'DELETE'])
def order_by_id(orderid):
    return


if __name__ == '__main__':
    app.run()
