import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# =====================
# ENV VARIABLES
# =====================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# =====================
# PASSWORD HASHING
# =====================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =====================
# PASSWORD FUNCTIONS
# =====================

def hash_password(password: str):
    """
    bcrypt safe fix (72 byte limit)
    """
    safe_password = password[:72]
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str):
    """
    verify hashed password safely
    """
    safe_password = plain_password[:72]
    return pwd_context.verify(safe_password, hashed_password)

# =====================
# JWT TOKEN
# =====================

def create_access_token(data: dict):
    """
    Create JWT token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# =====================
# OPTIONAL: VERIFY TOKEN
# =====================

def verify_token(token: str):
    """
    Decode JWT token
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None