from app.models.FormData import FormData


def generatePrompt(data: FormData) -> str:
  # Map boolean values to "Sim"/"Não"
  def boolToYesNo(x):
    return "Sim" if x else "Não"

  # Map enum values to their string representations
  def getEnumValue(x):
    return x.value if x else ""

  prompt = f"""
  Logo abaixo enviarei dados da resposta de um formulário de um paciente que irá fornecer as suas principais informações de saúde, nutrição, uso de remédios para doenças crônicas, rotina de sono, dentre outros aspectos.
  O seu objetivo é analisar todas as informações de maneira qualitativa para fornecer um feedback informativo com: possíveis deficiências nutricionais (de vitaminas, minerais, proteínas, etc.), os possíveis riscos de doenças que esse tipo de alimentação ou de rotina pode causar e se necessário, encaminhe o paciente para buscar ajuda com um profissional da área.
  O objetivo não é substituir o trabalho de médicos nutrólogos ou nutricionistas e sim auxiliar com a fase de triagem e o acompanhamento dos pacientes. Responda sempre levando em consideração a ética.

  1. Dados Gerais do Usuário
  Idade: {data.age}
  Sexo: {data.sex.value}
  Peso (kg): {data.weight_kg}
  Altura (cm): {data.height_cm}
  Cidade/Estado: {data.city}/{data.state}
  Histórico familiar: {data.family_medical_history}

  2. Hábitos Alimentares
  Frequência de consumo (últimos 30 dias):
  (diário, algumas vezes na semana, raramente, nunca)
  Tipos de alimentos consumidos:
  Frutas: {getEnumValue(data.fruits)}
  Vegetais: {getEnumValue(data.vegetables)}
  Grãos integrais: {getEnumValue(data.grains)}
  Proteínas animais: {getEnumValue(data.animal_proteins)}
  Proteínas vegetais: {getEnumValue(data.plant_proteins)}
  Laticínios: {getEnumValue(data.dairy)}
  Ultraprocessados: {getEnumValue(data.ultra_processed_foods)}
  Doces: {getEnumValue(data.sweets)}
  Água (L/dia): {data.water_intake_liters}

  3. Sintomas
  Nos últimos 30 dias, você experimentou algum dos seguintes sintomas:
  Fadiga: {boolToYesNo(data.fatigue)}
  Queda de cabelo: {boolToYesNo(data.hair_loss)}
  Pele ressecada: {boolToYesNo(data.dry_skin)}
  Problemas de visão: {boolToYesNo(data.vision_problems)}
  Unhas frágeis: {boolToYesNo(data.brittle_nails)}
  Alterações no apetite (aumento ou redução): {boolToYesNo(data.appetite_changes)}
  Dor muscular ou fraqueza: {boolToYesNo(data.muscle_pain)}
  Formigamento nas extremidades (mãos ou pés): {boolToYesNo(data.tingling_extremities)}
  Dificuldade de concentração: {boolToYesNo(data.difficulty_concentrating)}
  Outros (especifique): {data.other_symptoms}

  4. Uso de Medicamentos
  Você faz uso regular de medicamentos? {boolToYesNo(data.regular_medication_use)}
  Se sim, liste os medicamentos: {data.medications_list}
  Você faz uso regular de suplementos nutricionais ou vitamínicos? {boolToYesNo(data.taking_supplements)}
  Se sim, liste-os: {data.supplements_list}
  Frequência e dosagem: {data.frequency_dosage}

  5. Estilo de Vida
  Frequência de prática de atividades físicas: {data.physical_activity_frequency}
  Horas de sono por noite: {data.sleep_hours_per_night}
  Estresse percebido no dia a dia (entre baixo e moderado): {data.perceived_stress_level}

  6. Preferências e Restrições Alimentares
  Alimentos favoritos: {data.favorite_foods}
  Alimentos evitados: {data.avoided_foods}
  Alguma restrição alimentar? (alergia, intolerância, preferência cultural ou religiosa): {data.dietary_restrictions}

  7. Objetivo Nutricional
  O que você gostaria de alcançar com sua alimentação? {data.nutritional_goal}

  8. Consentimento e Uso de Dados
  Eu autorizo o uso dos meus dados de forma anônima para análises e pesquisas futuras. {data.consent_given}

  9. Observações ou Informações Adicionais
  Escreva aqui qualquer informação que considere importante para sua avaliação: {data.additional_notes}
  """

  return prompt.strip()
