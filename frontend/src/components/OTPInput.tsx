import { setUserMFA } from '../features/userSlice';
import { mfaOtpVerifyApi } from '../api/mfaOtpVerifyApi'
import React from 'react'
import OTPInput from 'react-otp-input';
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { useDispatch } from 'react-redux';
import { z } from 'zod';

const otpSchema = z.string().length(6).regex(/^[0-9]+$/, "OTP must be a 6-digit number");

function OTPInputComponent({otp, setOtp}: {
    otp: string | undefined;
    setOtp: React.Dispatch<React.SetStateAction<string | undefined>>
}) {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const handleOTPVerify = async(e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault()

        const validationResult = otpSchema.safeParse(otp);
        if (!validationResult.success) {
          toast.error(validationResult.error.errors[0].message);
          return;
    }

        if(otp) {
          const res = await mfaOtpVerifyApi(otp)
          if(res?.status === 'Success'){
            toast.success("OTP verification Succesful")
            dispatch(setUserMFA(true));
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
                    inputMode='numeric'
                    pattern="\d*"
                    onKeyDown={(e) => {
                      if (
                        !/^\d$/.test(e.key) && 
                        e.key !== 'Backspace' && 
                        e.key !== 'Delete' && 
                        e.key !== 'ArrowLeft' && 
                        e.key !== 'ArrowRight'
                      ) {
                        e.preventDefault();
                      }
                    }}
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