# tests/helpers.py
from google.genai import errors  # type: ignore


class DummyResponse:

  def __init__(self, text: str):
    self.text = text


class DummyAsyncModels:

  async def generate_content(self, model: str, contents: str) -> DummyResponse:
    return DummyResponse("Dummy AI response")


class DummyModels:

  def generate_content(self, model: str, contents: str) -> DummyResponse:
    return DummyResponse("Dummy AI response")


class DummyAio:

  def __init__(self):
    self.models = DummyAsyncModels()


class DummyClient:

  def __init__(self, api_key: str):
    self.models = DummyModels()
    self.aio = DummyAio()


class DummyAPIResponse:

  def __init__(self, status_code: int = 404):
    self.body_segments = [{
      "error": {
        "code": status_code,
        "message": f"dummy error message for {status_code}",
        "status": f"dummy status {status_code}"
      }
    }]
    self.status_code = status_code

  @property
  def response_json(self):
    return {
      "error": self.body_segments[0]["error"]
    }

class APIErrorFactory:

  @staticmethod
  def create_google_api_error(status_code: int = 404):
    """Helper to create properly configured APIError instances"""
    response = DummyAPIResponse(status_code)
    return errors.APIError(
      status_code=status_code,
      message=response.body_segments[0]["error"]["message"],
      response=response,
      response_json=response.response_json
    )
