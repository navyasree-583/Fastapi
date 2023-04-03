from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255), unique = True)
    quantity = Column(Integer)
    price = Column(Integer)
    
    
    
    



