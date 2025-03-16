import logo from '../../assets/logo.svg'
import './styles.css'

const Header = () => {
  return (
    <header>
      <div className="logo-container">
        <img src={logo} alt="Nutriagem Logo" className="logo" />
        <h1 className="logo-text">Nutriagem</h1>
      </div>
    </header>
  )
}

export default Header
