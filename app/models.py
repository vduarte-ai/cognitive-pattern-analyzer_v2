from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Thought(Base):

    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, index=True)

    text = Column(String)

    prediction = Column(String)

    confidence = Column(Float)

    confidence_label = Column(String)

    emotion = Column(String)

    timestamp = Column(String)
    

class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True)
    
    email = Column(String, unique=True)
    
    hashed_password = Column(String)
    
