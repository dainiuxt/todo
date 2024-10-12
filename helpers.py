def hash_password(password):
    """
        Get password from user in plain-text
        Generate salt for user
        Generate hash with salt and plain-text password
        Store hash result and salt to the DB

        Salt is unique to each user - reduces the risk of figuring out hash as each user has unique salt with which hash is generated.

        User provides password -> Retrieve salt -> Salt password -> Compare to stored hash -Matches-> Correct password, -Doesnt-> Wrong password
    """
    pass

