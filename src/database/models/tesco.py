from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Tesco(Base):
    __tablename__ = 'tesco_parser'
    id = Column(Integer, primary_key=True)
    product_url = Column(String)
    product_id = Column(Integer)
    image_url = Column(String)
    product_title = Column(String)
    category = Column(String)
    price = Column(String)
    product_description = Column(String)
    name_and_address = Column(String)
    return_address = Column(String)
    net_contents = Column(String)
    review = Column(Text)
    usually_bought_next_products = Column(Text)

