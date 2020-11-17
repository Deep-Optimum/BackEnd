from flask import Flask, request, Response
from datetime import datetime
from utils import data_tables, dbutils
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


@app.route('/posts/<listing_id>', methods=['PUT', 'DELETE'])
def post_by_id(listing_id):
    return


@app.route('/users', methods=['POST'])
def create_user():
    return


@app.route('/users/<uni>/listings', methods=['GET'])
def get_user_posts(uni):
    return


@app.route('/users/<uni>', methods=['GET', 'PUT'])
def user_by_uni(uni):
    return


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


@app.route('/orders/<order_id>', methods=['PUT', 'DELETE'])
def order_by_id(order_id):
    return


if __name__ == '__main__':
    app.run()
