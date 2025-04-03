import Header from './components/Header'
import Form from './components/Form'
import './index.css'

function App() {
  return (
    <div className="container">
      <Header />
      <main>
        <Form />
      </main>
      <footer>
        <p>&copy; {new Date().getFullYear()} Nutriagem - Todos os direitos reservados</p>
      </footer>
    </div>
  )
}

export default App
