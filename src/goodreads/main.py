"""
This module is the main function.
"""

# !/usr/bin/python3.8
import json
import sys
from argparse import ArgumentParser
import requests

from files_transform import *


def parse_arg():
    parser = ArgumentParser(description='spider of goodreads')

    "add args"
    parser.add_argument('--extract_db_to_file', '-e', action='store_true',
                        help='extract database as json files')
    # add args for GET/ PUT/ POST/ DELETE/ SEARCH
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('--scrapy', type=str, nargs=3,
                           metavar=('urls', 'book_num', 'author_num'),
                           default=(None, '20', '5'),
                           help='scrape books/authors given urls, book_num, author_num')
    arg_group.add_argument('--get', type=str, nargs=2,
                           metavar=('col', 'item_id'),
                           help='get item of collection given its id')
    arg_group.add_argument('--search', type=str,
                           help='search through database given query string')
    arg_group.add_argument('--delete', type=str, nargs=2,
                           metavar=('col', 'item_id'),
                           help='delete item given its item id')
    return parser


def get_request(col, item_id):
    """
    Send get reqeust to falsk to get html response
    :param col: given collection
    :param item_id: given item id
    """

    request = server_url + col
    response_info = requests.get(url=request, params={'id': item_id})

    print_response(response_info)


def delete_request(col, item_id):
    """
    DELETE request given collection and item_id
    :param col: collection
    :param item_id: id of item
    """

    request = server_url + col
    response_info = requests.delete(url=request,
                                    params={'id': item_id})
    print_response(response_info)


def search_request(query):
    """
    SearchId request. Would print http response
    :param query: given search query
    """
    request = server_url + 'search'
    response_info = requests.get(url=request,
                                 params={'q': query})
    print_response(response_info)

def print_response(response):
    """
    print function. get the response
    :param response: response
    """
    print(response)
    response = json.loads(response.content)
    print(response['results'])

def main(args):
    sys.path.append('.')
    sys.path.append('..')

    if args.extract_db_to_file:
        extract_db_to_json()

    elif args.scrapy[0]:
        book_num = int(args.scrapy[1])
        author_num = int(args.scrapy[2])
        if (book_num > 200) | (author_num > 50):
            print('Warning: numbers are too large.')

        cmd = "scrapy crawl goodreads -a urls=" + args.scrapy[0] + \
              " -a max_book=" + str(book_num) + \
              " -a max_author=" + str(author_num)
        os.system(cmd)

    # GET function
    elif args.get:
        get_request(*args.get)
    # SEARCH function
    elif args.search:
        search_request(args.search)
    # DELETE function
    elif args.delete:
        delete_request(*args.delete)

    print('finish')


if __name__ == '__main__':
    load_dotenv('goodreads/.env')
    header = {"Content-Type": "application/json"}
    server_url = os.environ.get('server_url')

    parser = parse_arg()
    args = parser.parse_args()
    main(args)
