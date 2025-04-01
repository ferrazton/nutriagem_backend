from fastapi import APIRouter, FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

from .routes import forms, health

appRouter = APIRouter()
appRouter.include_router(health.router)
appRouter.include_router(forms.router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(appRouter)
