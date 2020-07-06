from scrapy import Request, Spider
from json import loads
from items import ProductItem
from furl import furl
from logging import basicConfig
from datetime import datetime
from scrapy.utils.log import configure_logging


class TescoSpider(Spider):
    name = 'tesco'

    def __init__(self, url):
        super().__init__()
        configure_logging(install_root_handler=False)
        basicConfig(
            filename=datetime.now().strftime("%d-%m-%Y %H-%M-%S.log"),
        )
        self.url = url
        self.domain = 'https://www.tesco.com'
        self.product_template = 'https://www.tesco.com/groceries/products/'

    def start_requests(self):
        yield Request(url=self.url, callback=self.get_item_url, dont_filter=True)

    def get_item_url(self, response):
        for item in response.xpath('//h3/a/@href').getall():
            url = furl(self.domain).join(item).url
            yield Request(url=url, callback=self.get_item_reviews, dont_filter=True)
        if response.xpath('//nav[@class="pagination--page-selector-wrapper"]//li[last()]/a/@href').get() is not None:
            next_page_url = furl(self.domain).join(response.xpath(
                '//nav[@class="pagination--page-selector-wrapper"]//li[last()]/a/@href'
            ).get()).url
            yield Request(url=next_page_url, callback=self.get_item_url)

    def get_item_reviews(self, response):
        reviews_list = response.meta.get('reviews', None)
        if reviews_list is None:
            reviews = list()
        else:
            reviews = reviews_list
        for item in response.xpath('//article[@class="content"]/section'):
            title = item.xpath('h4/text()').get()
            stars_count = item.xpath('div//span/text()').get().split(' ')[0]
            author = item.xpath('//span[@class="nickname"]/text()').get()
            date = item.xpath('//span[@class="submission-time"]/text()').get()
            review_text = item.xpath('p[last()]/text()').get()
            reviews.append({
                'title': title,
                'stars_count': stars_count,
                'author': author,
                'date': date,
                'review_text': review_text
            })
        if response.xpath('//p[contains(@class, "base-components__BaseElement")]/a/@href'):
            next_page_review_url = furl(self.domain).join(response.xpath(
                '//p[contains(@class, "base-components__BaseElement")]/a/@href').get()).url
            yield Request(callback=self.get_item_reviews, url=next_page_review_url, dont_filter=True,
                          meta={'reviews': reviews})
        else:
            product_url = furl(response.url).remove(args=True, fragment=True).url
            yield Request(url=product_url, callback=self.get_item_contents, dont_filter=True,
                          meta={'reviews': reviews})

    def get_item_contents(self, response):
        product_id = response.url.rsplit('/', 1)[1]
        image_url = response.xpath('//div[@class="product-image__container"]/img/@src').get()
        image_url = image_url[:image_url.rfind('?')]
        product_title = response.xpath('//h1/text()').get()
        product_category = response.xpath(
            '(//span[contains(@class, "styled__StandaloneContainer")])[3]/a/span/span/text()').get()
        product_price = response.xpath('//span[@data-auto="price-value"]/text()').get()
        product_description = '\n'.join(
            response.xpath('//div[@id="product-description"]/*[not(self::h2)]//text()').getall())
        name_and_address = '\n'.join(response.xpath('//div[@id="manufacturer-address"]/ul/li/text()').getall())
        return_address = '\n'.join(response.xpath('//div[@id="return-address"]/ul/li/text()').getall())
        net_contents = response.xpath('//div[@id="net-contents"]/p/text()').get()
        usually_bought_next = list()
        json = loads(response.xpath('//body[@id="data-attributes"]/@data-redux-state').get())
        try:
            for item in json['productDetails']['recommendations']['data']:
                for _item in json['productDetails']['recommendations']['data'][item]['productItems']:
                    usually_bought_next.append({
                        'product_url': furl(self.product_template).join(_item['product']['id']).url,
                        'title': _item['product']['title'],
                        'product_image_url': _item['product']['defaultImageUrl'],
                        'price': _item['product']['price']
                    })
        except TypeError:
            usually_bought_next = None
        product = ProductItem()
        product['product_id'] = product_id
        product['url'] = response.url
        product['image_url'] = image_url
        product['title'] = product_title
        product['category'] = product_category
        product['price'] = product_price
        product['description'] = product_description
        product['name_and_address'] = name_and_address
        product['return_address'] = return_address
        product['net_contents'] = net_contents
        product['reviews'] = response.meta.get('reviews', None)
        product['usually_bought_next'] = usually_bought_next
        yield product
