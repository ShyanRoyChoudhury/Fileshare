
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import './App.css'
// import Upload from './components/Upload'
import SignInPage from './pages/SignIn'
import SignUpPage from './pages/Signup'
import DashboardPage from './pages/Dashboard'
import VerifyEmail from './pages/VerifyEmail'
import ProfilePage from './pages/Profile'

function App() {

  return (
    <>
      <Router>
        <Routes>
          {/* <Route path='/upload' element={<Upload />}/> */}
          <Route path='/signin' element={<SignInPage />}/>
          <Route path='/signup' element={<SignUpPage />}/>
          <Route path='/dashboard' element={<DashboardPage />}/>
          <Route path='/verifyEmail' element={<VerifyEmail />}/>
          <Route path='/profile' element={<ProfilePage />}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
