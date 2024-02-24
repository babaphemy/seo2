from pydantic import BaseModel,Field
class Seo(BaseModel):
    url: str = Field(min_length=6, description="Your website url")