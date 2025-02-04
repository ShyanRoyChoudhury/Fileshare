import { useEffect, useState } from "react"
import { getProfileApi } from "../api/getProfileApi"
import Navbar from "../components/Navbar"
import MfaQr from "../components/MfaQr"
import { useSelector } from "react-redux"
import { RootState } from "../store"

export default function MFAPage() {
  const [qrCode, setQrCode] = useState(null)
  const [email, setEmail] = useState("")
  
  const [name, setName] = useState<string | null>(null)
  const emailTest = useSelector((state: RootState) => state.user.email);
  async function getProfile(){
    const response = await getProfileApi()
    console.log('response?.data?.data?.qr_code', response)
    setQrCode(response?.qr_code)
    setEmail(response?.email)
    setName(response?.name)
  }
  console.log('test redux', emailTest)
  useEffect(()=> {
    getProfile()
  }, [])

  return (
    <div className="min-h-screen">
        <Navbar />
        
        <div className="flex justify-center">
        <div className="bg-white">
            
            {name}
            TEST: {emailTest}
            <MfaQr email={email} qrCode={qrCode}/>
        </div>
        </div>
    </div>
  )
}

