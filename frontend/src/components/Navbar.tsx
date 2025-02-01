import { LogOut } from "lucide-react"
import { logoutApi } from "../api/logoutApi"
import { useNavigate } from "react-router-dom"
function Navbar() {
    const navigate = useNavigate();
    const handleLogout = async () => {
        const res = await logoutApi()
        console.log('res', res)
        if(res.status === "Success") navigate('/signin')
    }
  return (
    <nav className=" shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="ml-8 text-3xl font-semibold text-white cursor-pointer" >FileShare</span>
            </div>
            <div className="flex items-center   rounded:md hover:opacity-60 " onClick={handleLogout}>
              <button className="flex space-x-2.5 py-2.5 px-4 rounded-md hover:bg-gray-500 items-center">
                <LogOut className="w-5 h-5 text-white"/>
                <span className="text-gray-200 ">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
  )
}

export default Navbar