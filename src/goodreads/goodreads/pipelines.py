"""
This module stores the crapied files into database.
"""
import os
import pathlib

import pymongo
from dotenv import load_dotenv
from itemadapter import ItemAdapter

def get_username_and_password():
    """
    get the dotenv username and password
    :return: username, password
    """
    load_dotenv(pathlib.Path('E:/2022fall/cs410/sracpy/sracpy/goodreads') / '.env')

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    print(f'Username is {username}, password is {password}!!! \n')
    # exit()
    return username, password

class GoodreadsPipeline:
    """
    In this class, the Items are stored into the mongo database.
    This structure is following the official tutorial
    """

    def __init__(self, mongo_uri, mongo_db):
        """
        Initiaolization of the whole class
        :param mongo_uri: mongodb uri
        :param mongo_db: mongodb database
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.bookid_set = set()
        self.authorid_set = set()
        self.datebase = None
        self.client = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        get the mongo uri and database from setting
        :param crawler: the spider
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        """
        Connect the spider to the database
        """
        username, password = get_username_and_password()
        self.client = pymongo.MongoClient(self.mongo_uri,
                                          username=username,
                                          password=password,
                                          authSource='admin')
        self.datebase = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        disconnect the spider and database
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        process the item, use id to insert to db.
        pass duplicated items
        :param item: Item to be stored
        :return: processed items
        """
        adapter = ItemAdapter(item)

        if "book_id" in adapter:
            if adapter["book_id"] not in self.bookid_set:
                self.bookid_set.add(adapter["book_id"])
                self.datebase["book"].insert_one(adapter.asdict())

        if "author_id" in adapter:
            if adapter["author_id"] not in self.authorid_set:
                self.bookid_set.add(adapter["author_id"])
                self.datebase["author"].insert_one(adapter.asdict())

        return item
