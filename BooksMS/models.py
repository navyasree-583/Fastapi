from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255), unique = True)
    price = Column(String(255))
    quantity = Column(Integer)
