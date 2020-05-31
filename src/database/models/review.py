from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Review(Base):
    __tablename__ = 'tesco_reviews'
    id = Column(Integer, primary_key=True)
    review_title = Column(String)
    stars_count = Column(Integer)
    author = Column(String)
    date = Column(String)
    review_text = Column(Text)
    parent_url = Column(String)
