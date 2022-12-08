"""
This module implements the Books and Authors Loader of Spider.
"""

import scrapy
from scrapy.item import Field
from itemloaders.processors import MapCompose, TakeFirst


def extract_num_from_string(string):
    """
    Given a string, extract the number it contains
    :param string: given string
    :return: the extracted number
    """
    digits = []
    for i in string:
        if i.isdigit():
            digits.append(i)
    return ''.join(digits)


class Author(scrapy.Item):
    """
    This class process the author id and take the first element of each Filed
    """
    name = Field(
        output_processor=TakeFirst()
    )
    author_url = Field(
        output_processor=TakeFirst()
    )
    author_id = Field(
        input_processor=MapCompose(extract_num_from_string),
        output_processor=TakeFirst()
    )
    rating = Field(
        output_processor=TakeFirst()
    )
    rating_count = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    review_count = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image_url = Field(
        output_processor=TakeFirst()
    )
    related_authors = Field()
    author_books = Field()


class Book(scrapy.Item):
    """
    This class take number from book id, title, rating,
    and take the first element of each Filed
    """
    book_url = Field(
        output_processor=TakeFirst()
    )
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    book_id = Field(
        input_processor=MapCompose(extract_num_from_string),
        output_processor=TakeFirst()
    )
    ISBN = Field(
        output_processor=TakeFirst()
    )
    author_url = Field(
        output_processor=TakeFirst()
    )
    author = Field(
        output_processor=TakeFirst()
    )
    rating = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    rating_count = Field(
        output_processor=TakeFirst()
    )
    review_count = Field(
        output_processor=TakeFirst()
    )
    image_url = Field(
        output_processor=TakeFirst()
    )
    similar_books = Field()
