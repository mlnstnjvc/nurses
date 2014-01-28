from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nurses.settings import *


engine = create_engine("postgresql://{user}:{password}@{host}/{database}".format(
    user = DB_USER,
    password = DB_PASSWORD,
    host =  DB_HOST,
    database = DB_NAME),
                       isolation_level=DB_ISOLATION_LEVEL)

Base = declarative_base()
Session = sessionmaker(bind=engine)




    
