from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1 import api
from app.core.config import settings
from app.database import engine
from app.services import Services

app = FastAPI(openapi_url=f'{settings.base_url}/openapi.json')


@app.middleware('http')
async def session_services(request: Request, call_next):
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        request.state.services = Services(session)
        response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api.api_router, prefix=settings.base_url)
print(app.routes)
