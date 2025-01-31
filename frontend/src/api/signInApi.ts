import axios from "axios"
import { BASE_URL } from "../config"

export const signInApi = async(idToken: string) => {
    try{
        const response = await axios.post(`${BASE_URL}/signin`, { idToken }, {
            headers: {
                "Content-Type": "application/json"
            },
            withCredentials: true
        })
        // if(response.data.status === 'Success'){
        return response.data;
        // }
        // return null;
    }catch(error){
        console.error("upload failed")
    }
}