import bcrypt

"""
    Get password from user in plain-text
    Generate salt for user
    Generate hash with salt and plain-text password
    Store hash result and salt to the DB

    Salt is unique to each user - reduces the risk of figuring out hash as each user has unique salt with which hash is generated.

    User provides password -> Retrieve salt -> Salt password -> Compare to stored hash -Matches-> Correct password, -Doesnt-> Wrong password
"""
def get_salt():
    return bcrypt.gensalt()

def hash_password(password, salt):

    # Convert password to array of bytes
    password = password.encode("utf-8")
    
    return bcrypt.hashpw(password, salt)

def check_password(entered_password_hash, stored_hash):
    return entered_password_hash == stored_hash