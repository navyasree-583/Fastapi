from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique = True)
    mobile=Column(String(255))
    password = Column(String(255))
    
    
    
    



