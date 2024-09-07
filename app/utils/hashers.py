import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def check_password(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password
    )
