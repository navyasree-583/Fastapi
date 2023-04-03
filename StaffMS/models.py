from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique = True)
    password = Column(String(255))
    mobile = Column(Integer)
