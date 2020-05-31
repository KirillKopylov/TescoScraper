from database.models.review import Review
from items.tesco.review_item import ReviewItem
from database import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class ReviewPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, ReviewItem):
            return item
        review = Review(
            review_title=item['review_title'],
            stars_count=item['stars_count'],
            author=item['author'],
            date=item['date'],
            review_text=item['review_text'],
            parent_url=item['parent_url'])
        session.add(review)
        session.commit()
        return item
