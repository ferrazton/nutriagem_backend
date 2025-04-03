import { useState } from 'react'
import axios from 'axios'
import PropTypes from 'prop-types';
import FormField from './FormField'
import Button from '../Button'
import './styles.css'

const NutritionResultsPopup = ({ isOpen, onClose, results }) => {
  if (!isOpen || !results) return null;

  return (
    <div className="popup-overlay">
      <div className="popup-container">
        <div className="popup-header">
          <h2>Análise Nutricional</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="popup-content">
          {results.title && (
            <div className="result-title">
              <h3>{results.title}</h3>
              {results.greeting && <p className="greeting">{results.greeting}</p>}
            </div>
          )}

          <div className="results-sections">
            {results.sections && results.sections.map((section, index) => (
              <div key={index} className="result-section">
                <h4>{section.title}</h4>
                <div className="section-content">
                  {section.content.map((item, i) => (
                    <p key={i} className={item.includes("**Pontos Positivos:**") ? "positive-point" :
                               item.includes("**Pontos de Atenção:**") ? "attention-point" : ""}>
                      {item}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="popup-footer">
          <button className="action-button close-action" onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

NutritionResultsPopup.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  results: PropTypes.shape({
    title: PropTypes.string,
    greeting: PropTypes.string,
    sections: PropTypes.arrayOf(
      PropTypes.shape({
        title: PropTypes.string.isRequired,
        content: PropTypes.arrayOf(PropTypes.string).isRequired
      })
    )
  })
};

NutritionResultsPopup.defaultProps = {
  results: null
};

const parseNutritionResults = (responseData) => {
  const sections = [];
  let currentSection = null;

  const title = responseData.title || "Análise Qualitativa das Informações do Paciente";
  const greeting = responseData.greeting || "Agradecemos por compartilhar suas informações detalhadas.";

  const lines = responseData.split('\n');

  lines.forEach(line => {
    if (line.includes('**') && line.includes(':')) {
      if (currentSection) {
        sections.push(currentSection);
      }
      currentSection = {
        title: line.trim(),
        content: []
      };
    } else if (currentSection && line.trim()) {
      currentSection.content.push(line.trim());
    }
  });

  if (currentSection) {
    sections.push(currentSection);
  }

  return { title, greeting, sections };
};

const Form = () => {
  const [formData, setFormData] = useState({
    // Section 1: General User Data
    age: '',
    sex: '',
    weight_kg: '',
    height_cm: '',
    state: '',
    city: '',
    family_medical_history: '',

    // Section 2: Dietary Habits
    fruits: '',
    vegetables: '',
    grains: '',
    animal_proteins: '',
    plant_proteins: '',
    dairy: '',
    ultra_processed_foods: '',
    sweets: '',
    water_intake_liters: '',
    special_dietary_practices: '',
    breakfast_time: '',
    lunch_time: '',
    dinner_time: '',
    snack_time: '',

    // Section 3: Symptoms
    fatigue: false,
    hair_loss: false,
    dry_skin: false,
    vision_problems: false,
    brittle_nails: false,
    appetite_changes: false,
    muscle_pain: false,
    tingling_extremities: false,
    difficulty_concentrating: false,
    other_symptoms: '',

    // Section 4: Medication
    regular_medication_use: false,
    medications_list: '',
    taking_supplements: false,
    supplements_list: '',
    frequency_dosage: '',

    // Section 5: Lifestyle
    physical_activity_frequency: '',
    sleep_hours_per_night: '',
    perceived_stress_level: '',

    // Section 6: Preferences
    favorite_foods: '',
    avoided_foods: '',
    dietary_restrictions: '',

    // Section 7-9: Goals/Consent/Notes
    nutritional_goal: '',
    consent_given: false,
    additional_notes: ''
  })
  const [showPopup, setShowPopup] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    let newValue = value
    if (type === 'number') {
      newValue = value === '' ? '' : Number(value)
    }
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : newValue
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Dados enviados:', formData);

    try {
      const response = await axios.post('http://127.0.0.1:8000/forms/', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });

      console.log('Ta Aqui a resposta:', response.data);
      setAnalysisResults(parseNutritionResults(response.data))
      setShowPopup(true);
    } catch (error) {
      console.error('Erro:', error.response ? error.response.data : error.message);
      alert('Erro ao enviar formulário. Por favor, tente novamente.');
    }
  };

  const sexOptions = [
    { value: 'Homem hetero', label: 'Homem hetero' },
    { value: 'Mulher hetero', label: 'Mulher hetero' },
    { value: 'Homem trans', label: 'Homem trans' },
    { value: 'Mulher trans', label: 'Mulher trans' },
    { value: 'Outro', label: 'Outro' }
  ]

  const dietaryFrequencyOptions = [
    { value: 'diário', label: 'Diário' },
    { value: 'algumas vezes na semana', label: 'Algumas vezes na semana' },
    { value: 'raramente', label: 'Raramente' },
    { value: 'nunca', label: 'Nunca' }
  ]

  const activityFrequencyOptions = [
    { value: 'diariamente', label: 'Diariamente' },
    { value: '3-4 vezes por semana', label: '3-4 vezes por semana' },
    { value: '1-2 vezes por semana', label: '1-2 vezes por semana' },
    { value: 'raramente', label: 'Raramente' },
    { value: 'nunca', label: 'Nunca' }
  ]

  const stressLevelOptions = [
    { value: 'baixo', label: 'Baixo' },
    { value: 'moderado', label: 'Moderado' },
    { value: 'alto', label: 'Alto' },
    { value: 'muito alto', label: 'Muito alto' }
  ]

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h2>Formulário de Avaliação Nutricional</h2>
        <p className="form-description">Preencha os campos abaixo para iniciarmos sua avaliação nutricional personalizada.</p>

        {/* Section 1: General User Data */}
        <div className="form-section">
          <h3>Dados Gerais</h3>

          <FormField
            label="Idade"
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />

          <FormField
            label="Sexo"
            type="select"
            name="sex"
            value={formData.sex}
            onChange={handleChange}
            options={sexOptions}
            required
          />

          <FormField
            label="Peso (kg)"
            type="number"
            name="weight_kg"
            value={formData.weight_kg}
            onChange={handleChange}
            step="0.1"
            placeholder="Ex: 70.5"
            required
          />

          <FormField
            label="Altura (cm)"
            type="number"
            name="height_cm"
            value={formData.height_cm}
            onChange={handleChange}
            placeholder="Ex: 170"
            required
          />

          <FormField
            label="Estado"
            name="state"
            value={formData.state}
            onChange={handleChange}
          />

          <FormField
            label="Cidade"
            name="city"
            value={formData.city}
            onChange={handleChange}
          />

          <FormField
            label="Histórico médico familiar"
            type="textarea"
            name="family_medical_history"
            value={formData.family_medical_history}
            onChange={handleChange}
            placeholder="Informe condições médicas presentes na família..."
          />
        </div>

        {/* Section 2: Dietary Habits */}
        <div className="form-section">
          <h3>Hábitos Alimentares</h3>

          <FormField
            label="Frutas"
            type="select"
            name="fruits"
            value={formData.fruits}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Vegetais"
            type="select"
            name="vegetables"
            value={formData.vegetables}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Grãos"
            type="select"
            name="grains"
            value={formData.grains}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Proteínas animais"
            type="select"
            name="animal_proteins"
            value={formData.animal_proteins}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Proteínas vegetais"
            type="select"
            name="plant_proteins"
            value={formData.plant_proteins}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Laticínios"
            type="select"
            name="dairy"
            value={formData.dairy}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Alimentos ultraprocessados"
            type="select"
            name="ultra_processed_foods"
            value={formData.ultra_processed_foods}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Doces"
            type="select"
            name="sweets"
            value={formData.sweets}
            onChange={handleChange}
            options={dietaryFrequencyOptions}
            required
          />

          <FormField
            label="Consumo de água (litros/dia)"
            type="number"
            name="water_intake_liters"
            value={formData.water_intake_liters}
            onChange={handleChange}
            step="0.1"
            placeholder="Ex: 2.5"
            required
          />

          <FormField
            label="Práticas alimentares especiais"
            name="special_dietary_practices"
            value={formData.special_dietary_practices}
            onChange={handleChange}
            placeholder="Ex: Jejum intermitente, dieta cetogênica..."
          />

          <div className="form-group">
            <h4>Horário das Refeições</h4>
            <FormField
              label="Café da manhã"
              type="time"
              name="breakfast_time"
              value={formData.breakfast_time}
              onChange={handleChange}
            />

            <FormField
              label="Almoço"
              type="time"
              name="lunch_time"
              value={formData.lunch_time}
              onChange={handleChange}
            />

            <FormField
              label="Jantar"
              type="time"
              name="dinner_time"
              value={formData.dinner_time}
              onChange={handleChange}
            />

            <FormField
              label="Lanches"
              type="time"
              name="snack_time"
              value={formData.snack_time}
              onChange={handleChange}
            />
          </div>
        </div>

        {/* Section 3: Symptoms */}
        <div className="form-section">
          <h3>Sintomas</h3>
          <p className="section-description">Selecione os sintomas que você tem apresentado recentemente:</p>

          <div className="checkbox-grid">
            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="fatigue"
                name="fatigue"
                checked={formData.fatigue}
                onChange={handleChange}
              />
              <label htmlFor="fatigue">Fadiga</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="hair_loss"
                name="hair_loss"
                checked={formData.hair_loss}
                onChange={handleChange}
              />
              <label htmlFor="hair_loss">Queda de cabelo</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="dry_skin"
                name="dry_skin"
                checked={formData.dry_skin}
                onChange={handleChange}
              />
              <label htmlFor="dry_skin">Pele seca</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="vision_problems"
                name="vision_problems"
                checked={formData.vision_problems}
                onChange={handleChange}
              />
              <label htmlFor="vision_problems">Problemas de visão</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="brittle_nails"
                name="brittle_nails"
                checked={formData.brittle_nails}
                onChange={handleChange}
              />
              <label htmlFor="brittle_nails">Unhas quebradiças</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="appetite_changes"
                name="appetite_changes"
                checked={formData.appetite_changes}
                onChange={handleChange}
              />
              <label htmlFor="appetite_changes">Mudanças no apetite</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="muscle_pain"
                name="muscle_pain"
                checked={formData.muscle_pain}
                onChange={handleChange}
              />
              <label htmlFor="muscle_pain">Dor muscular</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="tingling_extremities"
                name="tingling_extremities"
                checked={formData.tingling_extremities}
                onChange={handleChange}
              />
              <label htmlFor="tingling_extremities">Formigamento nas extremidades</label>
            </div>

            <div className="form-group-checkbox">
              <input
                type="checkbox"
                id="difficulty_concentrating"
                name="difficulty_concentrating"
                checked={formData.difficulty_concentrating}
                onChange={handleChange}
              />
              <label htmlFor="difficulty_concentrating">Dificuldade de concentração</label>
            </div>
          </div>

          <FormField
            label="Outros sintomas"
            type="textarea"
            name="other_symptoms"
            value={formData.other_symptoms}
            onChange={handleChange}
            placeholder="Descreva quaisquer outros sintomas que você tenha notado..."
          />
        </div>

        {/* Section 4: Medication */}
        <div className="form-section">
          <h3>Medicamentos e Suplementos</h3>

          <div className="form-group-checkbox">
            <input
              type="checkbox"
              id="regular_medication_use"
              name="regular_medication_use"
              checked={formData.regular_medication_use}
              onChange={handleChange}
            />
            <label htmlFor="regular_medication_use">Uso regular de medicamentos</label>
          </div>

          {formData.regular_medication_use && (
            <FormField
              label="Lista de medicamentos"
              type="textarea"
              name="medications_list"
              value={formData.medications_list}
              onChange={handleChange}
              placeholder="Liste os medicamentos que você utiliza regularmente..."
            />
          )}

          <div className="form-group-checkbox">
            <input
              type="checkbox"
              id="taking_supplements"
              name="taking_supplements"
              checked={formData.taking_supplements}
              onChange={handleChange}
            />
            <label htmlFor="taking_supplements">Uso de suplementos</label>
          </div>

          {formData.taking_supplements && (
            <>
              <FormField
                label="Lista de suplementos"
                type="textarea"
                name="supplements_list"
                value={formData.supplements_list}
                onChange={handleChange}
                placeholder="Liste os suplementos que você utiliza..."
              />

              <FormField
                label="Frequência e dosagem"
                name="frequency_dosage"
                value={formData.frequency_dosage}
                onChange={handleChange}
                placeholder="Ex: Whey protein - 1 scoop após o treino..."
              />
            </>
          )}
        </div>

        {/* Section 5: Lifestyle */}
        <div className="form-section">
          <h3>Estilo de Vida</h3>

          <FormField
            label="Frequência de atividade física"
            type="select"
            name="physical_activity_frequency"
            value={formData.physical_activity_frequency}
            onChange={handleChange}
            options={activityFrequencyOptions}
            required
          />

          <FormField
            label="Horas de sono por noite"
            type="number"
            name="sleep_hours_per_night"
            value={formData.sleep_hours_per_night}
            onChange={handleChange}
            min="1"
            max="24"
            required
          />

          <FormField
            label="Nível de estresse percebido"
            type="select"
            name="perceived_stress_level"
            value={formData.perceived_stress_level}
            onChange={handleChange}
            options={stressLevelOptions}
            required
          />
        </div>

        {/* Section 6: Preferences */}
        <div className="form-section">
          <h3>Preferências Alimentares</h3>

          <FormField
            label="Alimentos favoritos"
            type="textarea"
            name="favorite_foods"
            value={formData.favorite_foods}
            onChange={handleChange}
            placeholder="Liste seus alimentos favoritos..."
          />

          <FormField
            label="Alimentos evitados"
            type="textarea"
            name="avoided_foods"
            value={formData.avoided_foods}
            onChange={handleChange}
            placeholder="Liste alimentos que você prefere evitar..."
            required
          />

          <FormField
            label="Restrições alimentares"
            type="textarea"
            name="dietary_restrictions"
            value={formData.dietary_restrictions}
            onChange={handleChange}
            placeholder="Ex: Vegetariano, vegano, sem glúten, sem lactose..."
            required
          />
        </div>

        {/* Section 7-9: Goals/Consent/Notes */}
        <div className="form-section">
          <h3>Objetivos e Observações</h3>

          <FormField
            label="Objetivo nutricional"
            type="textarea"
            name="nutritional_goal"
            value={formData.nutritional_goal}
            onChange={handleChange}
            placeholder="Descreva seus objetivos nutricionais..."
          />

          <div className="form-group-checkbox consent-checkbox">
            <input
              type="checkbox"
              id="consent_given"
              name="consent_given"
              checked={formData.consent_given}
              onChange={handleChange}
              required
            />
            <label htmlFor="consent_given">
              Dou consentimento para o processamento dos meus dados para fins de avaliação nutricional
            </label>
          </div>

          <FormField
            label="Observações adicionais"
            type="textarea"
            name="additional_notes"
            value={formData.additional_notes}
            onChange={handleChange}
            placeholder="Compartilhe qualquer informação adicional que considere relevante..."
          />
        </div>

        <div className="form-actions">
          <Button type="submit" text="Enviar Formulário" />
        </div>
      </form>

      <NutritionResultsPopup
        isOpen={showPopup}
        onClose={() => setShowPopup(false)}
        results={analysisResults}
      />
    </>
  )
}

export default Form
