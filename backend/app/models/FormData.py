from pydantic import BaseModel
from models.GenderOptions import GenderOptions
from models.DietaryFrequency import DietaryFrequency

class FormData(BaseModel):
  #Section 1: General User Data
  age: int
  sex: GenderOptions
  weight_kg: float
  height_cm: int
  state: str = ""
  city: str = ""
  family_medical_history: str = ""
  
  #Section 2: Dietary Habits
  fruits: DietaryFrequency
  vegetables: DietaryFrequency
  grains: DietaryFrequency
  animal_proteins: DietaryFrequency
  plant_proteins: DietaryFrequency
  dairy: DietaryFrequency
  ultra_processed_foods: DietaryFrequency
  sweets: DietaryFrequency
  water_intake_liters: float
  special_dietary_practices: str = ""
  breakfast_time: str = ""
  lunch_time: str = ""
  dinner_time: str = ""
  snack_time: str = ""
  
  #Section 3: Symptoms
  fatigue: bool
  hair_loss: bool
  dry_skin: bool
  vision_problems: bool
  brittle_nails: bool
  appetite_changes: bool
  muscle_pain: bool
  tingling_extremities: bool
  difficulty_concentrating: bool
  other_symptoms: str = ""
  
  #Section 4: Medication
  regular_medication_use: bool
  medications_list: str = ""
  taking_supplements: bool
  supplements_list: str = ""
  frequency_dosage: str = ""
  
  #Section 5: Lifestyle
  physical_activity_frequency: str
  sleep_hours_per_night: int
  perceived_stress_level: str
  
  #Section 6: Preferences
  favorite_foods: str = ""
  avoided_foods: str
  dietary_restrictions: str
  
  #Section 7-9: Goals/Consent/Notes
  nutritional_goal: str = ""
  consent_given: bool
  additional_notes: str = ""
