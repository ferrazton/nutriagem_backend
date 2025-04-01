from fastapi import APIRouter  # type: ignore

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health():
  """
  Check if server is running.
  """

  return {"200": "OK"}
