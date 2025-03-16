import React from 'react'
import './styles.css'

const Button = ({ type = 'button', text, onClick, className = '', disabled = false }) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`btn ${className}`}
      disabled={disabled}
    >
      {text}
    </button>
  )
}

export default Button
