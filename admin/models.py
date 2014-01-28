from nurses.db import Base, Session
from sqlalchemy import Column, Integer, String, Boolean

class Nurse(Base):
    __tablename__ = "nurse"

    id = Column(Integer, primary_key = True,
                autoincrement = True)
    last_name = Column(String(200))
    first_name = Column(String(150))
    
    experienced = Column(Boolean(), default = False)
