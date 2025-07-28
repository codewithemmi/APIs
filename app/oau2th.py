import jwt
from datetime import datetime, timezone, timedelta
from . config import settings



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACESS_TOKEN_EXPIRE_MINUTES




def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode
