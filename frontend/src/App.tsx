
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import './App.css'
import Upload from './pages/Upload'
import SignInPage from './pages/SignIn'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/upload' element={<Upload />}/>
          <Route path='/signin' element={<SignInPage />}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
