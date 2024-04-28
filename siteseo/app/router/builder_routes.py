from fastapi import APIRouter,Depends
from siteseo.app.db.schema import WebbuilderRequest
from siteseo.app.service import builder
from sqlalchemy.orm import Session
from siteseo.app.db.session import get_db
router = APIRouter(
    prefix='/builder',
    tags=['website']
)
@router.post("/new")
def make_webfiles(web: WebbuilderRequest,db: Session = Depends(get_db)):
    return builder.builder_builder(db, web)
