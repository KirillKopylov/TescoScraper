import scrapy


class ReviewItem(scrapy.Item):
    review_title = scrapy.Field()
    stars_count = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    review_text = scrapy.Field()
    parent_url = scrapy.Field()
