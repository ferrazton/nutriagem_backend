import React from 'react'

const FormField = ({ label, type = 'text', name, value, onChange, placeholder = '', required = false, options = [] }) => {
  return (
    <div className="form-group">
      <label htmlFor={name}>{label}{required && <span className="required">*</span>}</label>

      {type === 'textarea' ? (
        <textarea
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
        />
      ) : type === 'select' ? (
        <select
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          required={required}
        >
          <option value="">Selecione uma opção</option>
          {options.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
        />
      )}
    </div>
  )
}

export default FormField
