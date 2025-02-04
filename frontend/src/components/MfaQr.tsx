import React, { useState } from 'react'
import { mfaOtpVerifyApi } from "../api/mfaOtpVerifyApi"
import { toast } from "react-toastify"
import { useNavigate } from 'react-router-dom'

type Props = {
    email: string,
    qrCode: any

}

function MfaQr({email, qrCode}: Props) {
    const [otp, setOtp] = useState<string | null>(null)
    const navigate = useNavigate()

    const handleOTPVerify = async(e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault()
        if(otp) {
          const res     = await mfaOtpVerifyApi(otp)
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
        <div>
            {qrCode? (
                <div>
                    <div>
                        <p>{email}</p>
                        <p>Enable 2FA with Google Authenticator App</p>
                        <img src={qrCode} alt="QR Code"/>
                    </div>
                    
                </div>
            ):
            (<p>Loading QR Code..</p>)
            }
            <label>
                Verify
            </label>
            <input type="number" placeholder="otp" className="border rounded"
            onChange={handleChange}
            ></input>
            <button onClick={handleOTPVerify}>Verify OTP</button>
        </div>
  )
}

export default MfaQr

