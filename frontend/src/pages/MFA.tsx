import { useEffect, useState } from "react"
import { getProfileApi } from "../api/getProfileApi"
import OTPInputComponent from "../components/OTPInput"

export default function MFAPage() {
  const [email, setEmail] = useState("")
  const [otp, setOtp] = useState<string | undefined>(undefined)

  async function getProfile(){
    const response = await getProfileApi()
    setEmail(response?.email)
  }
  useEffect(()=> {
    getProfile()
  }, [])
  return (
    <div className="min-h-screen">
        
        <div className="flex-col justify-center mt-20 mx-20 space-y-10">
        <h1 className="text-white flex items-center gap-x-2">
          <p className="text-5xl leading-none">Welcome,</p> 
          <p className="text-xl leading-none">{email}</p>
        </h1>

          <div className="bg-white p-6 space-y-4 rounded-md">
          <p className="font-semibold text-lg">Enter OTP FROM YOUR GOOGLE AUTHENTICATOR TO LOGIN</p>
            <OTPInputComponent otp={otp} setOtp={setOtp} />
          </div>
        </div>
    </div>
  )
}

