from flask import Flask, request, Response
from datetime import datetime
from utils import data_tables, dbutils
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'GET': 
        if not request.args.get['isbn', None]: 
            isbn = request.args['isbn']
        # get posts by isbn from database and store as array
        posts = []

        return {'posts': posts}, 200 if len(posts) else 404
    elif request.method == 'POST':
        post = request.get_json()

        # insert to database
        post_response = {}
        return {'post': post_response}, 204

@app.route('/posts/<post_id>', methods=['GET', 'PUT', 'DELETE'])
def get_post_by_id(post_id):

    if request.method == 'GET':
        # select post by post_id
        post = {}
        return  {'post': post}, 200 if len(post.keys()) else 404

    elif request.method == 'PUT':
        dict_to_update = request.get_json()
        # update db by post_id
        return {'message': 'updated successfully'}, 200

    elif request.method == 'DELETE':
        # delete row by post_id
        
        return {'message': 'deleted successfully'}, 200


@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    #insert user to db

    user_response = {}

    return {'user': user_response}, 201

@app.route('/users/<uni>', methods=['GET', 'PUT'])
def get_user_by_uni(uni):

    if request.method == 'GET':
        # select user by uni

        user = {}
        return {'user': user}, 200

    elif request.method == 'PUT':
        dict_to_update = request.get_json()
        # update db by uni
        
        return {'message': 'updated successfully'}, 200


@app.route('/users/<uni>/posts', methods=['GET'])
def get_user_posts(uni):
    # select posts by uni
    posts = []
    return {'posts': posts}, 200 if len(posts) else 404


@app.route('/users/<uni>/addresses', methods=['GET'])
def get_user_addresses(uni):
    # select addresses by uni

    addresses = []
    return {'addresses': addresses}, 200 if len(addresses) else 404


@app.route('/users/<uni>/orders', methods=['GET'])
def get_user_orders(uni):
    # select orders by uni

    orders = []
    return {'orders': orders}, 200 if len(orders) else 404


@app.route('/addresses', methods=['POST'])
def create_address():
    address = request.get_json()

    # insert address
    address_response = {}
    return {'address': address_response}, 201


@app.route('/addresses/<address_id>', methods=['PUT', 'DELETE'])
def modify_address_by_id(address_id):
    if request.method == 'PUT':
        dict_to_update = request.get_json()
        # update db by address_id
        
        return {'message': 'updated successfully'}, 200

    elif request.method == 'DELETE':
        # delete row by address_id
        
        return {'message': 'deleted successfully'}, 200



@app.route('/orders', methods=['POST'])
def create_order():
    order = request.get_json()

    # insert address
    order_response = {}
    return {'order': order_response}, 204
    return


@app.route('/orders/<order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(order_id):

    if request.method == 'GET':
        # select order by order_id

        order = {}
        return {'order': order}, 200

    elif request.method == 'PUT':
        dict_to_update = request.get_json()
        # update db by order_id
        
        return {'message': 'updated successfully'}, 200

    elif request.method == 'DELETE':
        # delete row by order_id
        
        return {'message': 'deleted successfully'}, 200



if __name__ == '__main__':
    app.run()
