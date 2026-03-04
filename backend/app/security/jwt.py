from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ------------------------------------------------------------------
# Token creators
# ------------------------------------------------------------------

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "access"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["exp"] = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------------------------------------------
# Token decoder
# ------------------------------------------------------------------

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])