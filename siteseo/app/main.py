from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import routes,home

seo_app = FastAPI()
seo_app.include_router(routes.router)
seo_app.include_router(home.router)
seo_app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000','http://164.90.145.100/','http://127.0.0.1/seo/'],
    allow_methods = ["*"],
    allow_credentials=True,
    allow_headers = ["*"]
)
