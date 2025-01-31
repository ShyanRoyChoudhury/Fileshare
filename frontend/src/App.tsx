
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import './App.css'
// import Upload from './components/Upload'
import SignInPage from './pages/SignIn'
import SignUpPage from './pages/Signup'
import DashboardPage from './pages/Dashboard'

function App() {

  return (
    <>
      <Router>
        <Routes>
          {/* <Route path='/upload' element={<Upload />}/> */}
          <Route path='/signin' element={<SignInPage />}/>
          <Route path='/signup' element={<SignUpPage />}/>
          <Route path='/dashboard' element={<DashboardPage />}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
