from scrapy import Item, Field


class ProductItem(Item):
    product_id = Field()
    url = Field()
    image_url = Field()
    title = Field()
    category = Field()
    price = Field()
    description = Field()
    name_and_address = Field()
    return_address = Field()
    net_contents = Field()
    reviews = Field()
    usually_bought_next = Field()
