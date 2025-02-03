import axios from "axios"
import { BASE_URL } from "../config"

export const mfaOtpVerifyApi = async(otp: string) => {
    try{
        const response = await axios.post(`${BASE_URL}/mfaOtpVerify`,{
            otp
        }, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        if(response.data.data.status === 'Success'){
            console.log('response in otp verify api', response)
            return response.data.data;
        }
        return null;
    }catch(error){
        console.error("get profile api failed")
    }
}