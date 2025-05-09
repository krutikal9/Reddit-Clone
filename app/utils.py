from bcrypt import hashpw, checkpw, gensalt

salt = gensalt()

def hash(password:str):
    hashed_password = hashpw(password.encode(),salt)
    return hashed_password.decode()

def compare(password:str, hash_password:str):
    compared_result = checkpw(password.encode(),hash_password.encode())
    return compared_result