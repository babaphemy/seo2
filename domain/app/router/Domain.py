from fastapi import APIRouter
from app.model.models import SeoRequest
from app.service import info_serv

router = APIRouter(
    prefix='/domain',
    tags=['domain']
)
@router.get('/info')
def domain_info():
    return {'message': 'Hello'}
@router.post('/spf')
def seo_result(req: SeoRequest):
    result = info_serv.check_spf_record(req.url)
    return {"message": result}