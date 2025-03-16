from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health():
  """
  Check if server is running.
  """

  return {"200": "OK"}
