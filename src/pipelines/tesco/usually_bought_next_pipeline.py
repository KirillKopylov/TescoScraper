from database.models.usually_bought_next import UsuallyBoughtNext
from items.tesco.usually_bought_next_item import UsuallyBoughtNextItem
from database import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class UsuallyBoughtNextPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, UsuallyBoughtNextItem):
            return item
        usually_bought_next = UsuallyBoughtNext(
            product_url=item['product_url'],
            product_title=item['product_title'],
            product_image_url=item['product_image_url'],
            price=item['price'],
            parent_url=item['parent_url']
        )
        session.add(usually_bought_next)
        session.commit()
        return item
