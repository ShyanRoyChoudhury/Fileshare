import { useEffect, useState } from "react"
import { getProfileApi } from "../api/getProfileApi"
import Navbar from "../components/Navbar"
import { mfaOtpVerifyApi } from "../api/mfaOtpVerifyApi"

export default function ProfilePage() {
  const [qrCode, setQrCode] = useState(null)
  const [email, setEmail] = useState(null)
  const [otp, setOtp] = useState<string | null>(null)
  async function getProfile(){
    const response = await getProfileApi()
    console.log('response?.data?.data?.qr_code', response)
    setQrCode(response?.qr_code)
    setEmail(response?.email)
  }

  useEffect(()=> {
    getProfile()
  }, [])

  const handleOTPVerify = async(e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    if(otp) {
        const res = await mfaOtpVerifyApi(otp)
        console.log('otp verify', res)
    }
  }
  const handleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
    setOtp(e.target.value)
  }
  return (
    <div className="min-h-screen">
        <Navbar />
        
        <div className="flex justify-center">
            <div className="bg-white">

            {qrCode? (
                <div>
                    <div>
                        <p>{email}</p>
                        <p>Enable 2FA with Google Authenticator App</p>
                        <img src={qrCode} alt="QR Code"/>
                    </div>
                    <div>
                        <label>
                            Verify
                        </label>
                        <input type="number" placeholder="otp" className="border rounded"
                        onChange={handleChange}
                        ></input>
                        <button onClick={handleOTPVerify}>Verify OTP</button>
                    </div>
                </div>
            ):
            (<p>Loading QR Code..</p>)
            }
            </div>
        </div>
    </div>
  )
}

