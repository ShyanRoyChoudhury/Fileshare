import { useEffect, useState } from "react"
import { getProfileApi } from "../api/getProfileApi"
import Navbar from "../components/Navbar"
import { mfaOtpVerifyApi } from "../api/mfaOtpVerifyApi"
import { useNavigate } from "react-router-dom"
import { toast } from "react-toastify"

export default function ProfilePage() {
  const [qrCode, setQrCode] = useState(null)
  const [email, setEmail] = useState<string | null>(null)
  const [otp, setOtp] = useState<string | null>(null)
  const [name, setName] = useState<string | null>(null)
  const navigate = useNavigate()
  async function getProfile(){
    const response = await getProfileApi()
    console.log('response?.data?.data?.qr_code', response)
    setQrCode(response?.qr_code)
    setEmail(response?.email)
    setName(response?.name)
  }

  useEffect(()=> {
    getProfile()
  }, [])

  const handleOTPVerify = async(e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    if(otp) {
      const res = await mfaOtpVerifyApi(otp)
      console.log('otp verify', res)
      console.log('res?.data?.status', res)
      if(res?.status === 'Success'){
        toast.success("OTP verification Succesful")
        navigate('/dashboard')
      }else{
        toast.error("OTP verification Failed")
      }
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

            {name}

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

