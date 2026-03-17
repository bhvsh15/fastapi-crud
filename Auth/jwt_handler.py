from jose import jwt
from datetime import datetime, timedelta

# Secret key for signing tokens
SECRET_KEY = "3ecce1e2fe24d806dcc6e752701dc4af5185de97899fae0cf2cd915f1fa50b8f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt