from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import routes,home,builder_routes

seo_app = FastAPI()
seo_app.include_router(routes.router)
seo_app.include_router(home.router)
seo_app.include_router(builder_routes.router)
seo_app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods = ["*"],
    allow_credentials=True,
    allow_headers = ["*"]
)
