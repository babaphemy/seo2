from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt,JWTError
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from siteseo.app.db.session import get_db
from siteseo.app.campus.app.info.service import get_userby_username
from siteseo.app.campus.app.info.models import Appuser
from fastapi import HTTPException,status

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = '2b49b0798c8174e4282de2be747b4b4434e8731c3f89f59d58ef4dfb4d948a60'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_data: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_data:
        expire = datetime.utcnow() + expires_data
    else :
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> Appuser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credential validation failed", 
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_userby_username(username, db)
    if user is None:
        raise credentials_exception
    return user