from .base import Base
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, JSON, TEXT, DECIMAL, TIMESTAMP
from sqlalchemy import Column, text


class Product(Base):
    __tablename__ = 'products'
    id = Column(BIGINT(unsigned=True), primary_key=True)
    product_id = Column(BIGINT(unsigned=True), index=True, unique=True)
    url = Column(VARCHAR(768))
    image_url = Column(VARCHAR(768))
    title = Column(VARCHAR(100))
    category = Column(VARCHAR(100))
    price = Column(DECIMAL(10, 3, unsigned=True))
    description = Column(TEXT)
    name_and_address = Column(TEXT)
    return_address = Column(TEXT)
    net_contents = Column(TEXT)
    reviews = Column(JSON)
    usually_bought_next = Column(JSON)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP()')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()')
