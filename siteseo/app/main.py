from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from siteseo.app.db.base import Base
from siteseo.app.db.session import engine
from siteseo.app.router import routes,home,builder_routes
from siteseo.app.campus.app.auth.auth import router as auth_router
from siteseo.app.campus.app.info import router
from siteseo.app.campus.app.classroom import routes as class_routes
from siteseo.app.campus.app.tranx import router as tranx_router
from siteseo.app.campus.app.messaging import routes as msg_route
from siteseo.app.campus.app.horace import router as horace_route


seo_app = FastAPI()
seo_app.include_router(routes.router)
seo_app.include_router(home.router)
seo_app.include_router(builder_routes.router)

seo_app.include_router(router.router)
seo_app.include_router(class_routes.router)
seo_app.include_router(tranx_router.router)
seo_app.include_router(msg_route.router)
seo_app.include_router(horace_route.router)
seo_app.include_router(horace_route.course_router)
seo_app.include_router(auth_router)

seo_app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods = ["*"],
    allow_credentials=True,
    allow_headers = ["*"]
)
Base.metadata.create_all(bind=engine)
