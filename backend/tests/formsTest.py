# tests/formsTest.py

import google.generativeai as genai  # type: ignore
import pytest
from app.main import apiRouter
from fastapi import FastAPI  # type: ignore
from httpx import AsyncClient  # type: ignore

app = FastAPI()
app.include_router(apiRouter)

valid_payload = {
    "age": 30,
    "sex": "Mulher hetero",
    "weight_kg": 70.5,
    "height_cm": 175,
    "state": "PE",
    "city": "Recife",
    "family_medical_history": "Nenhuma",
    "fruits": "diário",
    "vegetables": "diário",
    "grains": "diário",
    "animal_proteins": "diário",
    "plant_proteins": "algumas vezes na semana",
    "dairy": "algumas vezes na semana",
    "ultra_processed_foods": "rarely",
    "sweets": "rarely",
    "water_intake_liters": 2.5,
    "special_dietary_practices": "",
    "breakfast_time": "08:00",
    "lunch_time": "12:00",
    "dinner_time": "19:00",
    "snack_time": "16:00",
    "fatigue": False,
    "hair_loss": False,
    "dry_skin": False,
    "vision_problems": False,
    "brittle_nails": False,
    "appetite_changes": False,
    "muscle_pain": False,
    "tingling_extremities": False,
    "difficulty_concentrating": True,
    "other_symptoms": "Ansiedade",
    "regular_medication_use": False,
    "medications_list": "",
    "taking_supplements": False,
    "supplements_list": "",
    "frequency_dosage": "",
    "physical_activity_frequency": "3 vezes na semana",
    "sleep_hours_per_night": 7,
    "perceived_stress_level": "médio",
    "favorite_foods": "",
    "avoided_foods": "Frutos do mar",
    "dietary_restrictions": "Nenhuma",
    "nutritional_goal": "Saúde e hipertrofia",
    "consent_given": True,
    "additional_notes": "",
}


# Set a dummy API key for tests.
@pytest.fixture(autouse=True)
def set_dummy_api_key(monkeypatch):
  monkeypatch.setenv("GEMINI_API_KEY", "dummy_api_key")


# Dummy response to simulate Gemini API call.
class DummyResponse:

  def __init__(self, text):
    self.text = text


# Dummy generative model to avoid real external calls.
class DummyGenerativeModel:

  def __init__(self, model_name):
    self.model_name = model_name

  def generate_content(self, prompt):
    return DummyResponse("Dummy AI response")


# Override the generative model functions.
@pytest.fixture(autouse=True)
def override_gemini(monkeypatch):
  monkeypatch.setattr(genai, "GenerativeModel", lambda model_name: DummyGenerativeModel(model_name))
  monkeypatch.setattr(genai, "configure", lambda api_key: None)


# --- Tests ---


# 1. Test a successful /forms/ POST.
@pytest.mark.asyncio
async def test_analyze_form_success():
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/forms/", json=valid_payload)
  assert response.status_code == 200
  data = response.json()
  assert data.get("message") == "Form processed successfully"
  assert data.get("response") == "Dummy AI response"


# 2. Test missing API key (should return 401).
@pytest.mark.asyncio
async def test_analyze_form_missing_api_key(monkeypatch):
  monkeypatch.delenv("GEMINI_API_KEY", raising=False)
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/forms/", json=valid_payload)
  assert response.status_code == 401
  data = response.json()
  assert "Missing API key" in data.get("detail")


# 3. Test empty AI response: simulate generate_content returning an empty string.
@pytest.mark.asyncio
async def test_analyze_form_empty_response(monkeypatch):
  monkeypatch.setattr(DummyGenerativeModel, "generate_content", lambda self, prompt: DummyResponse(""))
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/forms/", json=valid_payload)
  assert response.status_code == 400
  data = response.json()
  assert "Empty response from AI model" in data.get("detail")


# 4. Test invalid payload: sending an empty JSON should trigger FastAPI/Pydantic validation errors.
@pytest.mark.asyncio
async def test_analyze_form_invalid_payload():
  async with AsyncClient(app=app, base_url="http://test") as ac:
    # Sending an empty JSON object should be invalid.
    response = await ac.post("/forms/", json={})
  # FastAPI returns 422 for request validation errors.
  assert response.status_code == 422


# 5. Test GoogleAPIError: simulate generate_content raising a GoogleAPIError.
@pytest.mark.asyncio
async def test_analyze_form_google_api_error(monkeypatch):

  def raise_google_api_error(self, prompt):
    raise genai.errors.GoogleAPIError("Test Google API error")

  monkeypatch.setattr(DummyGenerativeModel, "generate_content", raise_google_api_error)
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/forms/", json=valid_payload)
  assert response.status_code == 503
  data = response.json()
  assert "AI service unavailable" in data.get("detail")


# 6. Test unexpected error: simulate generate_content raising a generic exception.
@pytest.mark.asyncio
async def test_analyze_form_unexpected_error(monkeypatch):
  monkeypatch.setattr(
      DummyGenerativeModel,
      "generate_content",
      lambda self, prompt: (_ for _ in ()).throw(Exception("Test unexpected error")),
  )
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/forms/", json=valid_payload)
  assert response.status_code == 500
  data = response.json()
  assert "Internal server error" in data.get("detail")
