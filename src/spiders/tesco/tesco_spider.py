import scrapy
from items.tesco.tesco_item import TescoItem
from items.tesco.review_item import ReviewItem
from items.tesco.usually_bought_next_item import UsuallyBoughtNextItem
from urllib.parse import urljoin, urlparse


class TescoSpider(scrapy.Spider):
    name = 'tesco_spider'
    domain = 'https://tesco.com'
    url = 'https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.get_item_url)

    def get_item_url(self, response):
        for item in response.xpath('//div[@class="product-details--content"]/h3/a/@href'):
            product_url = self.domain + item.get()
            yield scrapy.Request(url=product_url, callback=self.get_item_attributes)
        next_page_url = response.xpath('//a[@name="go-to-results-page"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(url=self.domain + next_page_url, callback=self.get_item_url)

    def get_item_attributes(self, response):
        product_url = response.url
        product_id = product_url.rsplit('/', 1)[1]
        image_url = response.xpath('//div[@class="product-image__container"]/img/@src').get()
        image_url = image_url[:image_url.find('?')]
        product_title = response.xpath('//div[@class="product-details-tile__title-wrapper"]/h1/text()').get()
        category = response.xpath('//span[@class="styled__StandaloneContainer-sc-1xizymv-2'
                                  ' cZMcFx"]/a/span/span/text()')[2].get()
        price = response.xpath('//span[@class="value"]/text()').get()
        description = response.xpath('//div[@class="product-blocks"]/*')
        unnecessary_ids = ['return-address', 'net-contents', 'manufacturer-address']
        product_description = ''
        for item in description:
            if item.xpath('@id').get() not in unnecessary_ids:
                product_description += '\n' + '\n'.join(item.xpath('*//text()').getall())
            else:
                continue
        name_and_address = '\n'.join(response.xpath('//div[@id="manufacturer-address"]/ul/li/text()').getall())
        return_address = '\n'.join(response.xpath('//div[@id="return-address"]/ul/li/text()').getall())
        net_contents = response.xpath('//div[@id="net-contents"]/p/text()').get()
        tesco_item = TescoItem()
        tesco_item['product_url'] = product_url
        tesco_item['product_id'] = product_id
        tesco_item['image_url'] = image_url
        tesco_item['product_title'] = product_title
        tesco_item['category'] = category
        tesco_item['price'] = price
        tesco_item['product_description'] = product_description
        tesco_item['name_and_address'] = name_and_address
        tesco_item['return_address'] = return_address
        tesco_item['net_contents'] = net_contents
        yield tesco_item
        usually_bought_urls = response.xpath('//div[@class="tile-content"]/a/@href').getall()
        for item in usually_bought_urls:
            url = self.domain + item
            yield scrapy.Request(url=url, callback=self.get_usually_bought_next, meta={'parent_url': product_url},
                                 dont_filter=True)
        yield scrapy.Request(url=product_url, callback=self.get_product_reviews, dont_filter=True)

    def get_usually_bought_next(self, response):
        product_url = response.url
        product_title = response.xpath('//h1[@class="product-details-tile__title"]/text()').get()
        product_image_url = response.xpath('//div[@class="product-image__container"]/img/@src').get()
        product_image_url = product_image_url[:product_image_url.find('?')]
        product_price = response.xpath('//span[@class="value"]//text()').get()
        usually_bought_next_item = UsuallyBoughtNextItem()
        usually_bought_next_item['product_url'] = product_url
        usually_bought_next_item['product_title'] = product_title
        usually_bought_next_item['product_image_url'] = product_image_url
        usually_bought_next_item['price'] = product_price
        usually_bought_next_item['parent_url'] = response.meta['parent_url']
        yield usually_bought_next_item

    def get_product_reviews(self, response):
        reviews = response.xpath('//article[@class="content"]/*')
        for review in reviews:
            review_title = review.xpath('h4/text()').get()
            stars_count = review.xpath('div/span/text()').get()[0]
            review_author = review.xpath(
                'p[@class="base-components__BaseElement-sc-150tvch-0 sc-bbmXgH gWebBN typography__'
                '_styledElement-sc-186l0ce-0 gxVCAq"]/text()').get()
            if review_author is None:
                review_author = review.xpath('*/span[@class="nickname"]/text()').get()
            review_date = review.xpath('*/span[@class="submission-time"]/text()').get()
            review_text = review.xpath('p/text()').get()
            if review_text == review_author:
                review_text = review.xpath('p/text()').getall()[1]
            review_item = ReviewItem()
            review_item['review_title'] = review_title
            review_item['stars_count'] = stars_count
            review_item['author'] = review_author
            review_item['date'] = review_date
            review_item['review_text'] = review_text
            review_item['parent_url'] = urljoin(response.url, urlparse(response.url).path)
            yield review_item
        next_page_url = response.xpath('//a[@class="sc-tilXH iARkng styled_'
                                       '_TextButtonLink-ipdqot-0 GMOgz"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(url=self.domain + next_page_url, callback=self.get_product_reviews, dont_filter=True)
