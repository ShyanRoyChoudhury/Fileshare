import { useEffect, useState } from "react"
import { getProfileApi } from "../api/getProfileApi"
import { useSelector } from "react-redux"
import { RootState } from "../store"
import MfaQr from "@/components/MfaQr"
import OTPInputComponent from "@/components/OTPInput"

export default function ProfilePage() {
  const [qrCode, setQrCode] = useState(null)
  const [email, setEmail] = useState<string | null>(null)
  const [otp, setOtp] = useState<string | undefined>(undefined)
  const [_name, setName] = useState<string | null>(null)
  async function getProfile(){
    const response = await getProfileApi()
    console.log('response?.data?.data?.qr_code', response)
    setQrCode(response?.qr_code)
    setEmail(response?.email)
    setName(response?.name)
  }
  const emailTest = useSelector((state: RootState) => state.user.email);
  useEffect(()=> {
    getProfile()
  }, [])

  return (
    <div className="min-h-screen">
        
        <div className="flex justify-center mt-10">
            

            <div className="bg-white p-6">
            
            Email: {emailTest}
            <MfaQr email={email} qrCode={qrCode}/>
            <OTPInputComponent otp={otp} setOtp={setOtp} />
        </div>
        </div>
    </div>
  )
}

