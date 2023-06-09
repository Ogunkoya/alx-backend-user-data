#!/usr/bin/env python3

"""
This module defines the User model for the users table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): The integer primary key of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str or None): The session ID of the user, or None if not currently logged in.
        reset_token (str or None): The reset token for the user, or None if not requested.

    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)