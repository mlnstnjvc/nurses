from nurses.db import Base, Session
from sqlalchemy import Column, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref 
from datetime import datetime
# Create your models here.


class Scenario(Base):
    __tablename__ = "scenario"
    
    id_scenario = Column(String(256), primary_key=True)
    timestamp = Column(DateTime, default=datetime.now())

class Parameter(Base):
    __tablename__ = "parameter"

    id_par = Column(String(20), primary_key=True)
    id_scenario = Column(String(256), ForeignKey("scenario.id_scenario"), primary_key=True, nullable=True)
    scenario = relationship("Scenario", backref=backref("parameters"))
    
    number = Column(Float)
    text = Column(Text)
    
