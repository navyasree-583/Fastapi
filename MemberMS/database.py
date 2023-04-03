from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHAMY_DATABASE_URL ='mysql+pymysql://root:Admin2022@127.0.0.1:3306/membersdb'
# SQLALCHAMY_DATABASE_URL ='sqlite:///./blog.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

