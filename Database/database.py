from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "mysql+pymysql://root:Password#Error1511@localhost:3306/CRUD"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit = False, bind=engine, autoflush= False)
Base = declarative_base()
