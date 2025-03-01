import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from models.FormData import FormData
from utils.promptHelper import generatePrompt
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("/", response_class=HTMLResponse)
async def show_form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Formulário</title>
    </head>
    <body>
        <h1>Preencha o formulário:</h1>
        <form id="dataForm">
            <h2>Dados Gerais do Usuário</h2>
            <label>Idade: <input type="number" id="age"></label><br><br>
            <label>Sexo: 
                <select id="sex">
                    <option value="Homem hetero">Homem hetero</option>
                    <option value="Mulher hetero">Mulher hetero</option>
                    <option value="Homem trans">Homem trans</option>
                    <option value="Mulher trans">Mulher trans</option>
                    <option value="Outro">Outro</option>
                </select>
            </label><br><br>
            <label>Peso (kg): <input type="number" id="weight_kg"></label><br><br>
            <label>Altura (cm): <input type="number" id="height_cm"></label><br><br>
            <label>Estado: <input type="text" id="state"></label><br><br>
            <label>Cidade: <input type="text" id="city"></label><br><br>
            <label>Histórico médico familiar: <textarea id="family_medical_history"></textarea></label><br><br>
            
            <h2>Hábitos Alimentares</h2>
            <label>Frutas: 
                <select id="fruits">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Vegetais: 
                <select id="vegetables">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Grãos integrais: 
                <select id="grains">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Proteínas animais: 
                <select id="animal_proteins">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Proteínas vegetais: 
                <select id="plant_proteins">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Laticínios: 
                <select id="dairy">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Ultraprocessados: 
                <select id="ultra_processed_foods">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Doces: 
                <select id="sweets">
                    <option value="diário">diário</option>
                    <option value="algumas vezes na semana">Algumas vezes na semana</option>
                    <option value="raramente">Raramente</option>
                    <option value="nunca">Nunca</option>
                </select>
            </label><br><br>
            <label>Água (L/dia): <input type="number" id="water_intake_liters"></label><br><br>

            <h2>Sintomas</h2>
            <h3>Nos últimos 30 dias, você experimentou algum dos seguintes sintomas?</h3>
            <label><input type="checkbox" id="fatigue" name="fatigue"> Fadiga</label><br>
            <label><input type="checkbox" id="hair_loss" name="hair_loss"> Queda de cabelo</label><br>
            <label><input type="checkbox" id="dry_skin" name="dry_skin"> Pele ressecada</label><br>
            <label><input type="checkbox" id="vision_problems" name="vision_problems"> Problemas de visão</label><br>
            <label><input type="checkbox" id="brittle_nails" name="brittle_nails"> Unhas frágeis</label><br>
            <label><input type="checkbox" id="appetite_changes" name="appetite_changes"> Alterações no apetite (aumento ou redução)</label><br>
            <label><input type="checkbox" id="muscle_pain" name="muscle_pain"> Dor muscular ou fraqueza</label><br>
            <label><input type="checkbox" id="tingling_extremities" name="tingling_extremities"> Formigamento nas extremidades</label><br>
            <label><input type="checkbox" id="difficulty_concentrating" name="difficulty_concentrating"> Dificuldade de concentração</label><br><br>
            <label>Outros (especifique):</label><br>
            <textarea id="other_symptoms" name="other_symptoms" rows="4" cols="50"></textarea><br><br>

            <h2>Uso de Medicamentos</h2>
            <label><input type="checkbox" id="regular_medication_use" name="regular_medication_use"> Você faz uso regular de medicamentos?</label><br>
            <label>Se sim, liste os medicamentos:</label><br>
            <textarea id="medications_list" name="medications_list" rows="2" cols="50"></textarea><br><br>
            <label><input type="checkbox" id="taking_supplements" name="taking_supplements"> Você faz uso regular de suplementos nutricionais ou vitamínicos?</label><br>
            <label>List of Supplements:</label><br>
            <textarea id="supplements_list" name="supplements_list" rows="2" cols="50"></textarea><br><br>
            <label>Se sim, liste-os: </label><br>
            <input type="text" id="frequency_dosage" name="frequency_dosage"><br><br>
            
            <h2>Estilo de Vida</h2>
            <label>Frequência e prática de atividades físicas: </label><br>
            <select id="physical_activity_frequency" name="physical_activity_frequency">
                <option value="daily">Diariamente</option>
                <option value="couple_times_week">Algumas vezes na semana</option>
                <option value="rarely">Raramente</option>
                <option value="never">Nunca</option>
            </select><br><br>
            <label>Horas de sono por noite: </label><br>
            <input type="number" id="sleep_hours_per_night" name="sleep_hours_per_night" min="0" max="24"><br><br>
            <label>Estresse percebido no dia a dia (entre baixo e moderado):</label><br>
            <select id="perceived_stress_level" name="perceived_stress_level">
                <option value="low">Baixo</option>
                <option value="moderate">Moderado</option>
                <option value="high">Alto</option>
            </select><br><br>
            
            <h2>Preferências e Restrições Alimentares</h2>
            <label>Alimentos favoritos:</label><br>
            <textarea id="favorite_foods" name="favorite_foods" rows="2" cols="50"></textarea><br><br>
            <label>Alimentos evitados:</label><br>
            <textarea id="avoided_foods" name="avoided_foods" rows="2" cols="50"></textarea><br><br>
            <label>Alguma restrição alimentar? (alergia, intolerância, preferência cultural ou religiosa):</label><br>
            <textarea id="dietary_restrictions" name="dietary_restrictions" rows="2" cols="50"></textarea><br><br>

            <h2>Observações ou Informações Adicionais</h2>
            <label>Objetivo Nutricional:</label><br>
            <textarea id="nutritional_goal" name="nutritional_goal" rows="2" cols="50"></textarea><br><br>
            <label><input type="checkbox" id="consent_given" name="consent_given"> Eu autorizo o uso dos meus dados de forma anônima para análises e pesquisas futuras.</label><br><br>
            <label>Notas:</label><br>
            <textarea id="additional_notes" name="additional_notes" rows="3" cols="50"></textarea><br><br>

            <button type="submit">Enviar</button>
        </form>

        <script>
            document.getElementById("dataForm").addEventListener("submit", async function(event) {
                event.preventDefault(); // Prevent default form submission
                
                const formData = {
                    // Section 1: General User Data
                    age: document.getElementById("age").value,
                    sex: document.getElementById("sex").value,
                    weight_kg: parseFloat(document.getElementById("weight_kg").value),
                    height_cm: parseInt(document.getElementById("height_cm").value),
                    state: document.getElementById("state").value,
                    city: document.getElementById("city").value,
                    family_medical_history: document.getElementById("family_medical_history").value,

                    // Section 2: Dietary Habits
                    fruits: document.getElementById("fruits").value,
                    vegetables: document.getElementById("vegetables").value,
                    grains: document.getElementById("grains").value,
                    animal_proteins: document.getElementById("animal_proteins").value,
                    plant_proteins: document.getElementById("plant_proteins").value,
                    dairy: document.getElementById("dairy").value,
                    ultra_processed_foods: document.getElementById("ultra_processed_foods").value,
                    sweets: document.getElementById("sweets").value,
                    water_intake_liters: parseFloat(document.getElementById("water_intake_liters").value) || 0,

                    // Section 3: Symptoms
                    fatigue: document.getElementById("fatigue").checked,
                    hair_loss: document.getElementById("hair_loss").checked,
                    dry_skin: document.getElementById("dry_skin").checked,
                    vision_problems: document.getElementById("vision_problems").checked,
                    brittle_nails: document.getElementById("brittle_nails").checked,
                    appetite_changes: document.getElementById("appetite_changes").checked,
                    muscle_pain: document.getElementById("muscle_pain").checked,
                    tingling_extremities: document.getElementById("tingling_extremities").checked,
                    difficulty_concentrating: document.getElementById("difficulty_concentrating").checked,
                    other_symptoms: document.getElementById("other_symptoms").value,

                    // Section 4: Medication
                    regular_medication_use: document.getElementById("regular_medication_use").checked,
                    medications_list: document.getElementById("medications_list").value,
                    taking_supplements: document.getElementById("taking_supplements").checked,
                    supplements_list: document.getElementById("supplements_list").value,
                    frequency_dosage: document.getElementById("frequency_dosage").value,

                    // Section 5: Lifestyle
                    physical_activity_frequency: document.getElementById("physical_activity_frequency").value,
                    sleep_hours_per_night: parseInt(document.getElementById("sleep_hours_per_night").value),
                    perceived_stress_level: document.getElementById("perceived_stress_level").value,

                    // Section 6: Preferences
                    favorite_foods: document.getElementById("favorite_foods").value,
                    avoided_foods: document.getElementById("avoided_foods").value,
                    dietary_restrictions: document.getElementById("dietary_restrictions").value,

                    // Section 7-9: Goals, Consent, Notes
                    nutritional_goal: document.getElementById("nutritional_goal").value,
                    consent_given: document.getElementById("consent_given").checked,
                    additional_notes: document.getElementById("additional_notes").value
                };

                console.log("Submitting form with data:", formData);
                const response = await fetch("http://127.0.0.1:8000/forms/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();
                alert("Response: " + JSON.stringify(result));
            });
        </script>
    </body>
    </html>

    """

@router.post("/")
async def analyze_form(formData: FormData):
  # Generate LLM prompt
  llmPrompt = generatePrompt(formData)

  # LLM Integration
  genai.configure(api_key="$APIKEY") # Insert API Key here
  model = genai.GenerativeModel("gemini-1.5-flash") # or gemini-1.5-pro

  response = model.generate_content(llmPrompt)
  
  return {
    "message": "Form processed successfully",
    "response": response.text
  }
