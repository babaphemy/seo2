from fastapi import APIRouter,Depends, Query,Body,Path
from app.db.schema import WebbuilderRequest
from app.service import builder
from sqlalchemy.orm import Session
from app.db.session import get_db
router = APIRouter(
    prefix='/builder',
    tags=['website']
)
@router.post("/new")
def make_webfiles(web: WebbuilderRequest,db: Session = Depends(get_db)):
    return builder.builder_builder(db, web)
