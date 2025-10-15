from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
return pwd_context.hash(password)




def verify_password(plain: str, hashed: str) -> bool:
return pwd_context.verify(plain, hashed)




def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
to_encode = {"sub": subject}
expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
to_encode.update({"exp": expire})
return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)




def decode_token(token: str) -> dict:
return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])