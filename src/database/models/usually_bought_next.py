from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class UsuallyBoughtNext(Base):
    __tablename__ = 'tesco_usually_bought_next'
    id = Column(Integer, primary_key=True)
    product_url = Column(String)
    product_title = Column(Integer)
    product_image_url = Column(String)
    price = Column(String)
    parent_url = Column(String)
