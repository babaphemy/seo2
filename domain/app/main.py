from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import Domain


app = FastAPI()
app.include_router(Domain.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/')
async def index():
    return {'message': 'Welcome to ReachAI'}