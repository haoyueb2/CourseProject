from query import run_query, get_list
from flask_pymongo import PyMongo
from flask import Flask, request, make_response
from flask_cors import CORS
import flask
from dotenv import load_dotenv
import json
import os

import sys

from multidict import MultiDict

sys.path.append('.')
sys.path.append('..')
sys.path.append('../../goodreads/')


# Specify HTTP response code
HTTP_SUCCESS = 200
HTTP_BAD_REQUEST_ERROR = 400
HTTP_NOT_FOUND_ERROR = 404
HTTP_UNSUPPORTED_MEDIA_TYPE_ERROR = 415

SUCCESS_REQUEST_JSON = json.dumps({
    'code': HTTP_SUCCESS,
    'results': "Operation Successful!"
})

BAD_REQUEST_JSON = json.dumps({
    'code': HTTP_BAD_REQUEST_ERROR,
    'results': "Bad request error: invalid params!"
})

UNSUPPORTED_REQUEST_JSON = json.dumps({
    'code': HTTP_UNSUPPORTED_MEDIA_TYPE_ERROR,
    'results': "Unsupported Type! "
})

app = Flask(__name__)
CORS(app)


def create_app(testing=None):
    load_dotenv('../goodreads/.env')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    print(f'Username is {username}, password is {password}!!! \n')
    # exit()
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://localhost:27017/goodreads"
    )
    app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
    mongo = PyMongo(app)

    db = mongo.db
    author_col = mongo.db.author
    book_col = mongo.db.book

    if testing is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(testing)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'PUT', 'POST', 'DELETE'])
    def empty_response():
        """ When the response is empty """
        return flask.make_response(
            BAD_REQUEST_JSON, HTTP_BAD_REQUEST_ERROR
        )

    @app.route('/book', methods=['GET'])
    @app.route('/author', methods=['GET'])
    def get_item():
        """ get authors or books items given their corresponding id"""
        arg_num, item_id, col = parse_request()

        # id needs to be digit
        if item_id is None or arg_num != 1 or not item_id.isdigit():
            return flask.make_response(
                BAD_REQUEST_JSON, HTTP_BAD_REQUEST_ERROR
            )

        # use query function
        response_info = run_query('{}.{}_id:\"{}\"'.
                                  format(col, col, item_id), db)

        return make_response(json.dumps(response_info), response_info['code'])

    @app.route('/book', methods=['DELETE'])
    @app.route('/author', methods=['DELETE'])
    def delete_items():
        """ delete one item given item id"""

        arg_num, item_id, col = parse_request()

        # id needs to be digit
        if item_id is None or arg_num != 1 or not item_id.isdigit():
            return flask.make_response(BAD_REQUEST_JSON,
                                       HTTP_BAD_REQUEST_ERROR)
        id_query = get_id_query(col, item_id)
        if col == 'book':
            col = book_col
        else:
            col = author_col
        col.delete_many(id_query)
        return make_response(SUCCESS_REQUEST_JSON, HTTP_SUCCESS)

    @app.route('/scrape', methods=['POST'])
    def scrape_items():
        """ scrapy the books and authors given url """
        start_url = request.args.get('url')
        book_num = request.args.get('book_num', 1)
        author_num = 5
        print(start_url, book_num, author_num)
        if start_url is None:
            make_response(BAD_REQUEST_JSON, HTTP_BAD_REQUEST_ERROR)
        else:
            os.system('python E:/2022fall/cs410/sracpy/sracpy/goodreads/main.py '
                      '--scrapy '
                      '{} {} {}'.format(start_url, book_num, author_num))

        response_info = {
            'code': HTTP_SUCCESS,
            'results': 'Scraping Successful!'
        }

        return flask.make_response(
            json.dumps(response_info),
            response_info['code']
        )

    @app.route("/export", methods=['GET'])
    def export():
        os.system('python E:/2022fall/cs410/sracpy/sracpy/goodreads/main.py -e')
        response_info = {
            'code': HTTP_SUCCESS,
            'results': 'Export Successful!'
        }
        return flask.make_response(
            json.dumps(response_info),
            response_info['code']
        )

    @app.route('/search', methods=['GET'])
    def get_given_query():
        """ get author or books items given specific query"""
        query = request.args.get('q')

        # Will check whether there's only one argument
        if (query is None) or (len(list(request.args.keys())) != 1):
            return make_response(
                BAD_REQUEST_JSON, HTTP_BAD_REQUEST_ERROR
            )

        # use query function
        # response_info = run_query('{}.{}_id:\"{}\"'.
        #                           format(col, col, item_id), db)
        print('book.title:\"{}\"'.format(query))
        response_info = run_query('book.title:\"{}\"'.
                                  format(query), db)
        # response_info = run_query(query, db)

        return make_response(
            json.dumps(response_info),
            response_info['code']
        )

    @app.route('/vis/author', methods=['GET'])
    @app.route('/vis/book', methods=['GET'])
    def visualize_topk():
        """
        get the top k rating books / authors
        """
        col = request.path.split('/')[-1]
        k = request.args.get('k', 1)
        if col == 'book':
            col = book_col
        else:
            col = author_col
        a = 'rating'
        pipeline = [
            {'$addFields': {
                'double': {'$toDouble': f"${a}"}
            }},
            {'$sort': {'double': -1}},
            {'$limit': int(k)},
            {'$unset': 'double'}]
        data = col.aggregate(pipeline)
        data_lists = get_list(data)

        if len(data_lists) == 0:
            return make_response(json.dumps({
                'code': HTTP_NOT_FOUND_ERROR,
                'results': "No enough elements in specific collection! "
            }), HTTP_NOT_FOUND_ERROR)
        else:
            response_info = {
                'code': HTTP_SUCCESS,
                'results': data_lists
            }
            return make_response(
                json.dumps(response_info),
                response_info['code']
            )


def parse_request():
    """
    Parse the request
    """
    col = request.path[1:]
    item_id = request.args.get('id')
    arg_num = len(list(request.args.keys()))
    return arg_num, item_id, col


def get_id_query(col, item_id):
    """
    Get the id_query
    :param col: collection
    :param item_id: id
    :return: id_query
    """
    query = MultiDict()
    query.add('{}_id'.format(col), '{}'.format(item_id))
    return query


if __name__ == '__main__':
    create_app()
    app.debug = True
    app.run()
