import scrapy


class TescoItem(scrapy.Item):
    product_url = scrapy.Field()
    product_id = scrapy.Field()
    image_url = scrapy.Field()
    product_title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    product_description = scrapy.Field()
    name_and_address = scrapy.Field()
    return_address = scrapy.Field()
    net_contents = scrapy.Field()

