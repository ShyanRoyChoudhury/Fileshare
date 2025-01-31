import axios from "axios"
import { BASE_URL } from "../config"

export const signUpApi = async({idToken, email}: {
    idToken: string,
    email: string
}) => {
    try{
        const response = await axios.post(`${BASE_URL}/signUp`, { 
            idToken,
            email,
         }, {
            headers: {
                "Content-Type": "application/json"
            }
        })
        // if(response.data.status === 'Success'){
        return response.data;
        // }
        // return null;
    }catch(error){
        console.error("upload failed")
    }
}