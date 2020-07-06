from scrapy import signals
from database.models import Product
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, null
from sqlalchemy.dialects.mysql import insert


class ProductPipeline:
    def __init__(self):
        self.engine = create_engine(get_project_settings().get('DATABASE_URL'))
        self.connection = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        self.connection = self.engine.connect()

    def spider_closed(self, spider):
        self.connection.close()
        self.engine.dispose()

    def process_item(self, item, spider):
        result = {key: value if value is not None and len(value) != 0 else null() for key, value in item.items()}
        stmt = insert(Product).values(result)
        update_stmt = stmt.on_duplicate_key_update(
            product_id=stmt.inserted.product_id,
            url=stmt.inserted.url,
            image_url=stmt.inserted.image_url,
            title=stmt.inserted.title,
            category=stmt.inserted.category,
            price=stmt.inserted.price,
            description=stmt.inserted.description,
            name_and_address=stmt.inserted.name_and_address,
            return_address=stmt.inserted.return_address,
            net_contents=stmt.inserted.net_contents,
            reviews=stmt.inserted.reviews,
            usually_bought_next=stmt.inserted.usually_bought_next,
        )
        self.connection.execute(update_stmt)
        return item
