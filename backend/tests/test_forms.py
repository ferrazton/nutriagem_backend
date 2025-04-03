# tests/test_forms.py
import json

import pytest
from app.main import app
from app.models.DietaryFrequency import DietaryFrequency
from app.models.FormData import FormData
from app.models.GenderOptions import GenderOptions
from fastapi.testclient import TestClient  # type: ignore
from google import genai
from tests.helpers import (APIErrorFactory, DummyAsyncModels, DummyClient,
                           DummyResponse)

client = TestClient(app)

valid_payload = {
    "age": 30,
    "sex": GenderOptions.heterosexual_female.value,
    "weight_kg": 70.5,
    "height_cm": 175,
    "state": "PE",
    "city": "Recife",
    "family_medical_history": "Nenhuma",
    "fruits": DietaryFrequency.daily.value,
    "vegetables": DietaryFrequency.daily.value,
    "grains": DietaryFrequency.daily.value,
    "animal_proteins": DietaryFrequency.daily.value,
    "plant_proteins": DietaryFrequency.couple_times_week.value,
    "dairy": DietaryFrequency.couple_times_week.value,
    "ultra_processed_foods": DietaryFrequency.rarely.value,
    "sweets": DietaryFrequency.rarely.value,
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
def set_dummy_api_key(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setenv("GEMINI_API_KEY", "dummy_api_key")


# Override the Client with our dummy implementation.
@pytest.fixture(autouse=True)
def override_gemini(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(genai, "Client", lambda api_key: DummyClient(api_key))


# --- Test Cases ---


def test_analyze_form_success():
  response = client.post("/forms/", json=valid_payload)
  assert response.status_code == 200
  data = response.json()
  assert data.get("message") == "Form processed successfully"
  # Parse the JSON response
  response_content = json.loads(data["response"])
  assert response_content["analysis"] == "Dummy AI response"


def test_analyze_form_missing_api_key(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.delenv("GEMINI_API_KEY", raising=False)
  response = client.post("/forms/", json=valid_payload)
  assert response.status_code == 401
  assert "Missing API key" in response.json().get("detail")


def test_analyze_form_empty_response(monkeypatch: pytest.MonkeyPatch):

  async def empty_generate_content(self, model: str, contents: str):
    return DummyResponse("", valid_json=False)

  monkeypatch.setattr(DummyAsyncModels, "generate_content", empty_generate_content)
  response = client.post("/forms/", json=valid_payload)
  assert response.status_code == 400


def test_analyze_form_invalid_payload():
  response = client.post("/forms/", json={})
  assert response.status_code == 422
  # Check that the error message indicates missing required fields.
  assert "field required" in response.text.lower()


def test_analyze_form_google_api_error(monkeypatch: pytest.MonkeyPatch):

  async def raise_api_error(self, model: str, contents: str):
    raise APIErrorFactory.create_google_api_error(404)

  monkeypatch.setattr(DummyAsyncModels, "generate_content", raise_api_error)
  response = client.post("/forms/", json=valid_payload)
  # Our route catches APIError and raises a 503.
  assert response.status_code == 503
  assert "AI service unavailable" in response.json().get("detail")


def test_analyze_form_unexpected_error(monkeypatch: pytest.MonkeyPatch):

  async def raise_exception(self, model: str, contents: str):
    raise Exception("Test error")

  monkeypatch.setattr(DummyAsyncModels, "generate_content", raise_exception)
  response = client.post("/forms/", json=valid_payload)
  assert response.status_code == 500
  assert "Internal server error" in response.json().get("detail")


def test_analyze_form_invalid_ai_response(monkeypatch: pytest.MonkeyPatch):

  async def bad_response(self, model: str, contents: str):
    return DummyResponse("{invalid_json", valid_json=False)

  monkeypatch.setattr(DummyAsyncModels, "generate_content", bad_response)
  response = client.post("/forms/", json=valid_payload)
  assert response.status_code == 422
  assert "Invalid AI response format" in response.json().get("detail")


def test_medication_validation():

  invalid_payload = {
    **valid_payload,
    "regular_medication_use": True,
    "medications_list": ""
  }

  with pytest.raises(ValueError) as exc:
    FormData(**invalid_payload)
  assert "Medication list required" in str(exc.value)


def test_supplements_validation():

  invalid_payload = {
    **valid_payload,
    "taking_supplements": True,
    "supplements_list": ""
  }

  with pytest.raises(ValueError) as exc:
    FormData(**invalid_payload)
  assert "Supplements list required" in str(exc.value)
