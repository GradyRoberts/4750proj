import bcrypt


def hash_pwd(plain):
    return bcrypt.hashpw(
        plain.encode('utf-8'), 
        bcrypt.gensalt()) 

def check_pwd(plain, hashed):
    return bcrypt.checkpw(
        plain.encode('utf-8'),
        hashed)