import asyncio
import logging
import os

import google.generativeai as genai  # type: ignore
from app.models.FormData import FormData
from app.utils.promptHelper import generatePrompt
from dotenv import load_dotenv  # type: ignore
from fastapi import APIRouter, HTTPException  # type: ignore

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/forms", tags=["forms"])


@router.post("/")
async def analyze_form(formData: FormData):
  gemini_api_key = os.getenv("GEMINI_API_KEY")
  if not gemini_api_key:
    logger.error("Missing API key configuration")
    raise HTTPException(status_code=401, detail="Missing API key configuration")

  try:
    genai.configure(api_key=gemini_api_key)

    llmPrompt = generatePrompt(formData)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = await asyncio.to_thread(model.generate_content, llmPrompt)

    if not response.text:
      logger.error("Empty response from AI model")
      raise HTTPException(status_code=400, detail="Empty response from AI model")

    return {"message": "Form processed successfully", "response": response.text}

  except ValueError as ve:
    logger.error(f"Validation error: {str(ve)}")
    raise HTTPException(status_code=422, detail=str(ve))
  except genai.errors.GoogleAPIError as ge:
    logger.error(f"Google API error: {str(ge)}")
    raise HTTPException(status_code=503, detail="AI service unavailable")
  except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
