from typing import Any, Union

from pydantic import Field  # type: ignore
from pydantic import BaseModel, ConfigDict, field_validator  # type: ignore

from .DietaryFrequency import DietaryFrequency
from .GenderOptions import GenderOptions


class FormData(BaseModel):
  model_config = ConfigDict(extra='forbid', str_strip_whitespace=True, validate_default=True)

  # Section 1: General User Data
  age: int = Field(..., gt=0, le=120, json_schema_extra={"example": 30})
  sex: GenderOptions
  weight_kg: Union[float, int] = Field(..., gt=0, le=300, json_schema_extra={"example": 70.5})
  height_cm: Union[float, str] = Field(..., gt=50, le=250, json_schema_extra={"example": 175})
  state: str = Field(default="", max_length=2, pattern=r"^[A-Za-z]{2}$")
  city: str = Field(default="", max_length=30)
  family_medical_history: str = Field(default="", max_length=100)

  # Section 2: Dietary Habits
  fruits: DietaryFrequency
  vegetables: DietaryFrequency
  grains: DietaryFrequency
  animal_proteins: DietaryFrequency
  plant_proteins: DietaryFrequency
  dairy: DietaryFrequency
  ultra_processed_foods: DietaryFrequency
  sweets: DietaryFrequency
  water_intake_liters: Union[float, int] = Field(..., ge=0, le=20, json_schema_extra={"example": 2.5})
  special_dietary_practices: str = Field(default="", max_length=100)
  breakfast_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  lunch_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  dinner_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  snack_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")

  # Section 3: Symptoms
  fatigue: bool
  hair_loss: bool
  dry_skin: bool
  vision_problems: bool
  brittle_nails: bool
  appetite_changes: bool
  muscle_pain: bool
  tingling_extremities: bool
  difficulty_concentrating: bool
  other_symptoms: str = Field(default="", max_length=120)

  # Section 4: Medication
  regular_medication_use: bool
  medications_list: str = Field(default="", max_length=120)
  taking_supplements: bool
  supplements_list: str = Field(default="", max_length=120)
  frequency_dosage: str = Field(default="", max_length=100)

  # Section 5: Lifestyle
  physical_activity_frequency: str = Field(..., max_length=50)
  sleep_hours_per_night: Union[float, int] = Field(..., ge=0, le=24)
  perceived_stress_level: str = Field(..., max_length=50)

  # Section 6: Preferences
  favorite_foods: str = Field(default="", max_length=120)
  avoided_foods: str = Field(default="", max_length=120)
  dietary_restrictions: str = Field(default="", max_length=120)

  # Sections 7-9
  nutritional_goal: str = Field(default="", max_length=120)
  consent_given: bool
  additional_notes: str = Field(default="", max_length=200)

  @field_validator("medications_list")
  @classmethod
  def validate_medications(cls, v: str, values: Any) -> str:
    if values.data.get("regular_medication_use") and not v.strip():
      raise ValueError("Medication list required when using regular medication")
    return v.strip()

  @field_validator("supplements_list")
  @classmethod
  def validate_supplements(cls, v: str, values: Any) -> str:
    if values.data.get("taking_supplements") and not v.strip():
      raise ValueError("Supplements list required when taking supplements")
    return v.strip()

  @field_validator("*", mode="before")
  @classmethod
  def strip_strings(cls, v: Any) -> Any:
    if isinstance(v, str):
      return v.strip()
    return v
