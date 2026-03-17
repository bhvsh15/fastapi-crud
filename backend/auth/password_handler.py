from passlib.context import CryptContext

# bcrypt hashing algorithm
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Hash a new password before saving to database
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)