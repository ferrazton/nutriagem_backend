from enum import Enum


class DietaryFrequency(str, Enum):
  daily = "diário"
  couple_times_week = "algumas vezes na semana"
  rarely = "raramente"
  never = "nunca"
