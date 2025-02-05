import React, { useState } from 'react'
import { mfaOtpVerifyApi } from "../api/mfaOtpVerifyApi"
import { toast } from "react-toastify"
import { useNavigate } from 'react-router-dom'
import OTPInput from 'react-otp-input'
import OTPInputComponent from './OTPInput'
// import OTPInput from 'otp-input-react'
type Props = {
    email: string | null,
    qrCode: any

}

function MfaQr({email, qrCode}: Props) {

    
    // const handleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
    //   setOtp(e.target.value)
    // }

  return (
        <div className='p-6'>
            {qrCode? (
                <div>
                    <div>
                        <p>Scan & Enter OTP on Google Authenticator App to Enable 2FA Authentication</p>
                        <img src={qrCode} alt="QR Code"/>
                    </div>
                    
                </div>
            ):
            (<p>Loading QR Code..</p>)
            }
        </div>
  )
}

export default MfaQr

