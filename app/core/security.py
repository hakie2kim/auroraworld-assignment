import time
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_utils.tasks import repeat_every
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"  # 실제 프로덕션에서는 환경 변수 등으로 안전하게 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 블랙리스트를 저장할 set - 실제 구현에서는 데이터베이스 사용
token_used = set()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@repeat_every(seconds=60*60*24)  # 24시간마다 실행
def clean_token_blacklist():
    token_used.clear()
