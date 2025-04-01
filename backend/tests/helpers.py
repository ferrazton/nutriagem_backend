# tests/helpers.py


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

  def __init__(self):
    self.body_segments = [{"error": {"code": 404, "message": "dummy error message", "status": "dummy status"}}]
