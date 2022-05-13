from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.bell import api as bell
from backend.core.settings import settings

settings.configure_logging()

app = FastAPI(**settings.fastapi_kwargs)

if settings.allowed_hosts:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.on_event("startup")
async def startup_event():
    print("Starting up...")


app.include_router(bell.router)
