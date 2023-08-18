#!/usr/bin/env python3
"""_summary_ - SQLAlchemy model named User for a database table named users
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
Base = declarative_base()


class User(Base):
    """_summary_
    SQLAlchemy model named User for a database table named users
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
