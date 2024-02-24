from pydantic import BaseModel
class SeoRequest(BaseModel):
    url: str