import { mfaOtpVerifyApi } from '@/api/mfaOtpVerifyApi'
import React from 'react'
import OTPInput from 'react-otp-input';
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'

function OTPInputComponent({otp, setOtp}: {
    otp: string | undefined;
    setOtp: React.Dispatch<React.SetStateAction<string | undefined>>
}) {
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
  return (
    <div>

<div className='flex-col px-6'>
              <div className='flex space-y-2 justify-center'>
                <OTPInput
                  value={otp}
                  onChange={setOtp}
                  numInputs={6}
                  renderSeparator={<span style={{ margin: '0 5px' }}>-</span>}
                  renderInput={(props) => (
                    <input
                    {...props}
                    style={{
                      width: '40px',
                      height: '40px',
                      margin: '0',
                      textAlign: 'center',
                      border: '1px solid #ccc',
                      borderRadius: '5px',
                      fontSize: '18px',
                    }}
                    />
                  )}
                  containerStyle={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: '10px', // Adds spacing between input boxes
                    padding: '10px',
                  }}
                />

              </div>
          
              <button onClick={handleOTPVerify} className='w-full py-3 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-300 ease-in-out flex items-center justify-center'>
                Verify OTP
              </button>
            </div>
    </div>
  )
}

export default OTPInputComponent