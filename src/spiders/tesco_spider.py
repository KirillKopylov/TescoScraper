import scrapy
import json


class TescoSpider(scrapy.Spider):
    name = 'tesco_spider'
    domain = 'https://tesco.com'
    # url = 'https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all'
    debug_url = 'https://www.tesco.com/groceries/en-GB/products/258509257'
    usually_bought_next = list()
    review = list()

    def start_requests(self):
        # yield scrapy.Request(url=self.url, callback=self.get_item_url)
        yield scrapy.Request(url=self.debug_url, callback=self.get_item_attributes)

    def get_item_url(self, response):
        # for item in response.xpath('//div[@class="product-details--content"]/h3/a/@href'):
        #     url = self.domain + item.get()
        #     yield scrapy.Request(url=url, callback=self.get_item_attributes)
        yield scrapy.Request(url=self.debug_url, callback=self.get_item_attributes)

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
                product_description += '\n' + '\n'.join(item.xpath('*/*/text()').getall())
            else:
                continue
        name_and_address = '\n'.join(response.xpath('//div[@id="manufacturer-address"]/ul/li/text()').getall())
        return_address = '\n'.join(response.xpath('//div[@id="return-address"]/ul/li/text()').getall())
        net_contents = response.xpath('//div[@id="net-contents"]/p/text()').get()
        usually_bought_urls = response.xpath('//div[@class="tile-content"]/a/@href').getall()
        for item in usually_bought_urls:
            url = self.domain + item
            yield scrapy.Request(url=url, callback=self.get_usually_bought_next)
        request = scrapy.Request(url=product_url, callback=self.get_product_reviews, dont_filter=True)
        request.meta['product_id'] = product_id
        request.meta['image_url'] = image_url
        request.meta['product_title'] = product_title
        request.meta['category'] = category
        request.meta['price'] = price
        request.meta['product_description'] = product_description
        request.meta['name_and_address'] = name_and_address
        request.meta['return_address'] = return_address
        request.meta['net_contents'] = net_contents
        yield request

    def get_usually_bought_next(self, response):
        product_url = response.url
        product_title = response.xpath('//h1[@class="product-details-tile__title"]/text()').get()
        product_image_url = response.xpath('//div[@class="product-image__container"]/img/@src').get()
        product_image_url = product_image_url[:product_image_url.find('?')]
        product_price = response.xpath('//span[@class="value"]//text()').get()
        values = {
            'usually_bought_next_product': {
                'product_url': product_url,
                'product_title': product_title,
                'product_image_url': product_image_url,
                'product_price': product_price
            }
        }
        self.usually_bought_next.append(values)

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
            values = {
                'review': {
                    'review_title': review_title,
                    'stars_count': stars_count,
                    'author': review_author,
                    'date': review_date,
                    'review_text': review_text
                }
            }
            self.review.append(values)
        url = response.xpath('//a[@class="sc-tilXH iARkng styled__TextButtonLink-ipdqot-0 GMOgz"]/@href').get()
        if url is not None:
            yield scrapy.Request(url=self.domain + url, callback=self.get_product_reviews)
        else:
            print(json.dumps(self.usually_bought_next))
            print(json.dumps(self.review))
