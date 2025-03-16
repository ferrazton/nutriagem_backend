from enum import Enum


class GenderOptions(str, Enum):
  heterosexual_female = "Mulher hetero"
  heterosexual_male = "Homem hetero"
  trans_female = "Mulher trans"
  trans_male = "Homem trans"
  other = "Outro"
