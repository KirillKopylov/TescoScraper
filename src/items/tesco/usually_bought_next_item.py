import scrapy


class UsuallyBoughtNextItem(scrapy.Item):
    product_url = scrapy.Field()
    product_title = scrapy.Field()
    product_image_url = scrapy.Field()
    price = scrapy.Field()
    parent_url = scrapy.Field()
