from fastapi import APIRouter  # type: ignore
from routes import forms, health

apiRouter = APIRouter()
apiRouter.include_router(health.router)
apiRouter.include_router(forms.router)
