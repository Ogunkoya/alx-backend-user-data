#!/usr/bin/env python3
import bcrypt

def hash_password(password):
    '''
    function returns a salted, hashed password, which is a byte string.
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def is_valid(hashed_password, password):
    '''
    function that expects 2 arguments and returns a boolean
    '''
    return bcrypt.checkpw(password.encode(), hashed_password)