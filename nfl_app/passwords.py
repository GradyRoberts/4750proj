"""
Functions for hashing and checking passwords.
"""

import bcrypt

from nfl_app.users import retrieve_pwd_hash


def hash_pwd(plain):
    plain_enc = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_enc, salt)


def check_pwd(email, plain):
    plain_enc = plain.encode("utf-8")
    hashed = retrieve_pwd_hash(email).encode("utf-8")
    return bcrypt.checkpw(plain_enc, hashed)
