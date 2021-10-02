from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base 


class Contact(Base):
    __tablename__ = "contact"
    name = Column(String , index = True)
    email = Column(String, primary_key=True,unique=True)