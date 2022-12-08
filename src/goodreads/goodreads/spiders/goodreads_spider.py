"""
This module implements the Spider for good reads.
"""

from scrapy import Spider
from scrapy.loader import ItemLoader

from goodreads.items import Author, Book


def parse_book_info(loader, response):
    """
    get all information from current book page
    :param loader: item loader of book item
    :param response: pages of books
    """
    loader.add_value('book_url', response.url)
    loader.add_xpath('title', "//h1[@id='bookTitle']/text()")
    loader.add_value('book_id', response.url)
    loader.add_xpath('ISBN', '//*[@itemprop="isbn"]/text()')
    loader.add_xpath('author_url', "//a[@class='authorName']/@href")
    loader.add_xpath('author', "//a[@class='authorName']/span/text()")
    loader.add_xpath('rating', "//span[@itemprop='ratingValue']/text()")
    loader.add_xpath('rating_count', "//meta[@itemprop='ratingCount']/@content")
    loader.add_xpath('review_count', "//meta[@itemprop='reviewCount']/@content")
    loader.add_xpath('image_url', "//img[@id='coverImage']/@src")
    loader.add_xpath('similar_books', "//li[@class='cover']/a/img/@alt")


def parse_author_info(loader, response):
    """
    get all information from current author page
    :param loader: item loader of author item
    :param response: pages of author
    """
    loader.add_xpath('name', "//h1[@class='authorName']"
                             "/span[@itemprop='name']/text()")
    loader.add_value('author_url', response.url)
    loader.add_value('author_id', response.url)
    loader.add_css('rating', "span.average::text")
    loader.add_xpath('rating_count', '//span[@class="value-title"]'
                                     '[@itemprop="ratingCount"]/text()')
    loader.add_xpath('review_count', '//span[@class="value-title"]'
                                     '[@itemprop="reviewCount"]/text()')
    loader.add_xpath('image_url', '//div[@class="leftContainer authorLeftContainer"]'
                                  '/a/img/@src')
    loader.add_xpath('author_books', '//span[@itemprop="name"]'
                                     '[@role="heading"]/text()')


class GoodReadsSpider(Spider):
    """
    This class implements the Spider for goodreads.
    It contains parse function for scraped information.
    """
    name = "goodreads"

    def __init__(self, *args, **kwargs):
        """
        Initialization of the spider
        :param args: user argument
        :param kwargs: user argument keys
        """
        super().__init__(*args, **kwargs)
        try:
            urls = kwargs.pop('urls')
            self.max_book = int(kwargs.pop('max_book'))
            self.max_author = int(kwargs.pop('max_author'))
            self.start_urls = urls.split(',')
        except KeyError:
            raise RuntimeError('Need to give at least one goodreads url,'
                               ' max book and author numbers!')

    def parse(self, response, **kwargs):
        """
        parse the response
        :param response: the book pages
        """

        # Now begin to scrape the author information
        author_url = response.xpath("//a[@class='authorName']/@href").extract()[0]
        if author_url is not None:
            yield response.follow(author_url, callback=self.parse_author)

        book_loader = ItemLoader(item=Book(), response=response)
        parse_book_info(book_loader, response)
        yield book_loader.load_item()

        # Have loaded this book into database. Now try to find more books and author
        try:
            similar_books_url = response.xpath("//a[contains(text(), "
                                               "'See similar books…')]/@href").extract()[0]
            yield response.follow(similar_books_url, callback=self.parse_similar_books)
        except IndexError:
            pass

    def parse_author(self, response):
        """
        get informaiton from the page of the author
        :param response: pages of authors
        """
        author_loader = ItemLoader(item=Author(), response=response)
        parse_author_info(author_loader, response)

        # Have loaded this author into database except the related authors names.
        try:
            url_similar_author = response.xpath('//div[@class="hreview-aggregate"]/a'
                                                '[contains(text(), '
                                                '"Similar authors")]/@href').extract()[0]

            yield response.follow(url_similar_author,
                                  callback=self.get_similar_author_names,
                                  meta={'item': author_loader.load_item()})
        except IndexError:
            yield author_loader.load_item()

        # Have loaded this author into database. Now try to find more author
        try:
            similar_author_urls = response.xpath('//div[@class="hreview-aggregate"]/a'
                                                 '[contains(text(), '
                                                 '"Similar authors")]/@href').extract()[0]
            yield response.follow(similar_author_urls,
                                  callback=self.parse_similar_authors)
        except IndexError:
            pass

        # # Have loaded this author into database. Now try to find related books
        # url_books = response.xpath("//a[@class='bookTitle'][@itemprop='url']/@href").extract()
        # for url in url_books:
        #     if url.startswith('/book/show/'):
        #         yield response.follow(url, callback=self.parse)

    def get_similar_author_names(self, response):
        """
        add the names of the authors, and yield item
        :param response: the page of similar authors
        """
        loader = ItemLoader(item=response.meta['item'], response=response)
        loader.add_xpath("related_authors", "//a[@class='gr-h3 gr-h3--serif gr-h3--"
                                            "noMargin']/span[@itemprop='name']/text()")
        yield loader.load_item()

    def parse_similar_books(self, response):
        """
        parse the books that are similar to the book that initiates the request
        :param response: page listed similar books
        """
        urls = response.xpath("//div[@class='responsiveBook__media']/a/@href").extract()
        yield from response.follow_all(urls, callback=self.parse)

    def parse_similar_authors(self, response):
        """
        Parge simlar authors, to keep scripying
        :param response: the page of similar authors
        """
        urls = response.xpath("//a[@class='gr-h3 gr-h3--serif gr-h3--noMargin']/@href").extract()
        yield from response.follow_all(urls, callback=self.parse_author)
