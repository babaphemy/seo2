from typing import List,Optional
from fastapi import APIRouter, Query,Path
from siteseo.app.service import seo_serv
from siteseo.app.service import play_serv
from siteseo.app.db.schema import Seo

router = APIRouter(
    prefix='/seo',
    tags=['seo']
)

@router.post('/info')
def seo_info(seo: Seo) -> dict:
    result = seo_serv.get_page_info(seo.url)
    return {'detail': result}
@router.post('/result')
def seo_result(seo: str):
    return seo_serv.get_page_info(seo)
@router.post('/friendly')
def url_friendliness(seo: Seo) -> dict:
    return seo_serv.handle_friendly_url(seo.url)
@router.post('/images')
def image_test(seo: Seo) -> dict:
    return play_serv.check_image(seo.url)
@router.post('/deprecated')
def deprecated_html(v: Optional[List[str]] = Query(None)):
    return {"version": v}
@router.post('/analysis/{sid}')
def object_analysis(sid: int = Path(...,gt=5, le=10, lt=8) ):
    return {"sid": sid}
@router.post('/socials')
def social_media():
    pass
def dom_optimization():
    pass
def ssl_check():
    pass