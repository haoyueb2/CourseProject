"""
This file implements the query functions
"""

import re

# Specify HTTP response status code
HTTP_SUCCESS = 200
HTTP_BAD_REQUEST_ERROR = 400
HTTP_NOT_FOUND_ERROR = 404
HTTP_UNSUPPORTED_MEDIA_TYPE_ERROR = 415

# Basic configuration of the query syntex
QUERY_SPLIT = "(?P<first>[^ \n].+) (?P<and_logic>OR｜AND) (?P<second>[^ \n].+)"
QUERY_BASIC = "(?P<col>book|author).(?P<field>[^ \n:]*): *(?P<content>.+)"
QUERY_CONTENT = "(?P<logic>NOT )?(?P<expression>.+)"

BOOK_KEYS = [
    'book_url', 'title', 'book_id', 'ISBN',
    'author_url', 'author', 'rating', 'rating_count',
    'review_count', 'image_url', 'similar_books'
]

AUTHOR_KEYS = [
    'name', 'author_url', 'author_id', 'rating',
    'rating_count', 'review_count', 'image_url',
    'related_authors', 'author_books'
]


def parse_query(query):
    """
    parse the query into logics, and contents
    :param query: given query
    :return: if it success, return the got items, else return Error results.
             Both successful / fail results would be like:
                    - status code (200 / 404 / ...)
                    - results
    """
    # basic content format check
    match_split = re.fullmatch(QUERY_SPLIT, query)
    match_split_second = None
    if match_split is not None:
        match_split_first = match_split['first']
        match_split_second = match_split['second']
    else:
        match_split_first = query
    match_basic_first = re.fullmatch(QUERY_BASIC, match_split_first)

    if match_basic_first is None:
        return {
                   'code': HTTP_BAD_REQUEST_ERROR,
                   'results': "Invalid input! The format should follow <book>|<author>.<field_name>:<...>"
               }, None

    col_1 = match_basic_first['col']
    field_1 = match_basic_first['field']
    content_1 = match_basic_first['content']
    field_2 = None
    if match_split_second is not None:
        match_basic_second = re.fullmatch(QUERY_BASIC, match_split_second)
        col_2 = match_basic_second['col']
        field_2 = match_basic_second['field']
        content_2 = match_basic_second['content']

        # Check col
        if col_1 != col_2:
            return {'code': HTTP_BAD_REQUEST_ERROR,
                    'results': 'two colletions should be the same!'}
    col = col_1

    # Check the field
    log = check_field(col, field_1, field_2)
    if log is not None:
        return log, None

    log = parse_content_from_right(field_1, content_1)
    if match_split_second is not None:
        log_second = parse_content_from_right(field_2, content_2)
        if log_second['code'] != HTTP_SUCCESS:
            return log
        if match_split['and_logic'] == 'AND':
            log['results'] = "{{ \"$and\":[ {}, {} ]  }}".format(log['results'], log_second['results'])
        else:
            log['results'] = "{{ \"$or\":[ {}, {} ]  }}".format(log['results'], log_second['results'])

    return log, col


def check_field(col, field_1, field_2):
    """
    Would check whether the field is correct
    :param col: collection
    :param field: field
    :return: report
    """
    if col == 'author':
        if (field_1 not in AUTHOR_KEYS) or \
                ((field_2 is not None) and (field_2 not in AUTHOR_KEYS)):
            return {
                'code': HTTP_BAD_REQUEST_ERROR,
                'results': "Invalid input! Authors collection doesn't contain this field."
            }
    else:
        if (field_1 not in BOOK_KEYS) or \
                ((field_2 is not None) and (field_2 not in BOOK_KEYS)):
            return {
                'code': HTTP_BAD_REQUEST_ERROR,
                'results': "Invalid input! Books collection doesn't contain this field."
            }


def get_expression_command(field, expression, logic, log):
    """
    Get the command of expression
    """
    sql_command = log['results']

    # handle greater/equal
    if expression[0] == '>' or expression[0] == '<':
        num = expression[1:].strip()

        if re.fullmatch('[0-9]+\.?[0-9]*', num) is None:
            return {
                'code': HTTP_UNSUPPORTED_MEDIA_TYPE_ERROR,
                'results': 'Is not number!'
            }
        if expression[0] == '>':
            log['results'] = "{{ \"$gt\": \"{}\" }}" \
                .format(expression.strip()[1:])
        else:
            log['results'] = "{{ \"$lt\": \"{}\" }}" \
                .format(expression.strip()[1:])
    elif (expression[0] == '\"') and (expression[-1] == '\"'):
        log['results'] = "\"{}\" " \
            .format(expression.strip()[1:-1])
    elif (expression[0] != '\"') and (expression[-1] != '\"'):
        log['results'] = "{{ \"$regex\": \"{}\" }}" \
            .format(expression.strip())
    else:
        return {
            'code': HTTP_BAD_REQUEST_ERROR,
            'results': 'Quotes are wrong!'
        }

    if logic is None:
        log['results'] = "{{ \"{}\": {} }}".format(field, log['results'])
    else:
        log['results'] = "{{ \"{}\":  {{ \"$not\" {}  }}}}".format(field, log['results'])
    return log


def parse_content_from_right(field, content):
    """
    Parse the content into command
    :param field: field name
    :param content: content
    :return: log that contains status code and command
    """
    log = {
        'code': HTTP_SUCCESS,
        'results': None,
    }
    # Now begin to parse the content
    match_content = re.fullmatch(QUERY_CONTENT, content)
    if match_content is None:
        return {
            'code': HTTP_BAD_REQUEST_ERROR,
            'results': "The command is wrong! logic operator seems to be mixed with keywords."
        }

    match_content = match_content.groupdict()

    log = get_expression_command(field, match_content['expression'],
                                 match_content.get('logic', None), log)
    return log


def run_query(query, database):
    """
    process given query
    Args:
        - query: given query
        - database: mongodb
    Return:
        a dict that contains:
            lists of extracted data.
            status code
    """

    query_info, col = parse_query(query)
    col = eval("database.{}".format(col))
    # invalid input
    if query_info['code'] != HTTP_SUCCESS:
        return query_info

    query_info['results'] = 'col.find({})'.format(query_info['results'])
    data = eval(query_info['results'])
    data_lists = get_list(data)

    if len(data_lists) == 0:
        return {
            'code': HTTP_NOT_FOUND_ERROR,
            'results': 'no item in database satisfies the requirement'
        }

    return {
        'code': HTTP_SUCCESS,
        'results': data_lists
    }


def get_list(data):
    """
    Get list of the data
    :param data: extracted data
    :return: list of data
    """
    data_list = []
    for i in data:
        i.pop('_id')
        data_list.append(i)
    return data_list
