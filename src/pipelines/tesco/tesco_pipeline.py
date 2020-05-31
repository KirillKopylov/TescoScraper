from database.models.tesco import Tesco
from items.tesco.tesco_item import TescoItem
from database import engine
from sqlalchemy.orm import sessionmaker
from database.models.review import Review
from database.models.usually_bought_next import UsuallyBoughtNext
import json

Session = sessionmaker(bind=engine)
session = Session()


class TescoPipeline:
    def open_spider(self, spider):
        session.execute('TRUNCATE TABLE tesco_parser')
        session.commit()

    def process_item(self, item, spider):
        if not isinstance(item, TescoItem):
            return item
        tesco = Tesco(product_url=item['product_url'],
                      product_id=item['product_id'],
                      image_url=item['image_url'],
                      product_title=item['product_title'],
                      category=item['category'],
                      price=item['price'],
                      product_description=item['product_description'],
                      name_and_address=item['name_and_address'],
                      return_address=item['return_address'],
                      net_contents=item['net_contents'])
        session.add(tesco)
        session.commit()
        return item

    def close_spider(self, spider):
        for tesco in session.query(Tesco):
            reviews = list()
            usually_bought_next = list()
            for review in session.query(Review).filter_by(parent_url=tesco.product_url):
                values = {
                    'review': {
                        'review_title': review.review_title,
                        'stars_count': review.stars_count,
                        'author': review.author,
                        'date': review.date,
                        'review_text': review.review_text
                    }
                }
                reviews.append(values)
            for bought_next in session.query(UsuallyBoughtNext).filter_by(parent_url=tesco.product_url):
                values = {
                    'usually_bought_next_product': {
                        'product_url': bought_next.product_url,
                        'product_title': bought_next.product_title,
                        'product_image_url': bought_next.product_image_url,
                        'price': bought_next.price
                    }
                }
                usually_bought_next.append(values)
            tesco.review = json.dumps(reviews)
            tesco.usually_bought_next_products = json.dumps(usually_bought_next)
            session.add(tesco)
            session.commit()
        session.execute('TRUNCATE TABLE tesco_reviews')
        session.execute('TRUNCATE TABLE tesco_usually_bought_next')
        session.commit()
