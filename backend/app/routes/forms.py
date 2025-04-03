import logging
import os

from app.models.FormData import FormData
from app.utils.promptHelper import generatePrompt
from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, HTTPException  # type: ignore
from google import genai
from google.genai import errors  # type: ignore

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/forms", tags=["forms"])


@router.post("/")
async def analyze_form(formData: FormData):
  gemini_api_key = os.getenv("GEMINI_API_KEY")
  if not gemini_api_key:
    logger.error("Missing API key configuration")
    raise HTTPException(status_code=401, detail="Missing API key configuration")

  try:
    client = genai.Client(api_key=gemini_api_key)

    llmPrompt = generatePrompt(formData)
    response = await client.aio.models.generate_content(
      model="gemini-2.0-flash",
      contents=llmPrompt
    )

    if not response.text:
      logger.error("Empty response from AI model")
      raise HTTPException(status_code=400, detail="Empty response from AI model")

    return {"message": "Form processed successfully", "response": response.text}

  except HTTPException:
    raise
  except ValueError as ve:
    logger.error(f"Validation error: {str(ve)}")
    raise HTTPException(status_code=422, detail=str(ve))
  except errors.APIError as ge:
    logger.error(f"Google API error: {str(ge)}")
    raise HTTPException(status_code=503, detail="AI service unavailable")
  except Exception as e:
    error_detail = ""
    if hasattr(e, "response"):
      if hasattr(e.response, "body_segments") and isinstance(e.response.body_segments, list) and len(
          e.response.body_segments) > 0:
        error_json = e.response.body_segments[0].get("error", {})
        error_detail = error_json.get("message", str(e))
    else:
      error_detail = str(e)
    logger.error(f"Unexpected error: {error_detail}")
    raise HTTPException(status_code=500, detail="Internal server error")
