from fastapi import APIRouter, HTTPException,status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from siteseo.app.db.session import get_db
from siteseo.app.campus.app.auth.oauth2 import create_access_token
from siteseo.app.campus.app.info.models import Appuser
from siteseo.app.campus.app.util.converter import verify_password
router = APIRouter(
    tags=['authentication']
)
@router.post('/token')
def get_auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Appuser).filter(Appuser.email == request.username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not verify_password(request.password, user.password):
         raise HTTPException(status_code=403, detail="Access denied! Invalid credentials")
    access_token = create_access_token(data={'sub': user.email})
    return {
         'access_token': access_token,
         'token_type': 'bearer',
         'user_id': user.id,
         'username': user.email
    }