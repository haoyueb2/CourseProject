"""
This module tracks the number of books and authors,
and control the spider.
"""

import logging
from scrapy import signals

logger = logging.getLogger(__name__)


class SpiderCountNum:
    """
    This class control the maximum book and author scrapied
    """

    def __init__(self, crawler):
        self.book_count = 0
        self.author_count = 0
        self.crawler = crawler
        self.max_book = None
        self.max_author = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Initialize class. Connect crawler to this class
        :param crawler: spider
        :return: this class object
        """
        # instantiate the extension object
        ext = cls(crawler)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        return ext

    def spider_opened(self, spider):
        """
        Open spider. Get max infomation
        :param spider: spider
        """
        self.max_book = min(spider.max_book, 2000)
        self.max_author = min(spider.max_author, 2000)
        logger.info("opened spider %s", spider.name)

    def spider_closed(self, spider):
        """
        Log close information
        """
        logger.info("closed spider %s", spider.name)

    def item_scraped(self, item, spider):
        """
        Track item number. When it reaches maximum, stop the spider.
        :param item: scrapied item
        :param spider: spider
        """
        if "ISBN" in item:
            self.book_count += 1
        if "author_id" in item:
            self.author_count += 1

        if (self.book_count > self.max_book) & (self.author_count > self.max_author):
            logger.info("get maximum number")
            self.crawler.engine.close_spider(spider)
