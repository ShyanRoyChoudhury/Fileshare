import axios from "axios"
import { BASE_URL } from "../config"

export const logoutApi = async() => {
    try{
        const response = await axios.get(`${BASE_URL}/logout`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        if(response.data.data.status === 'Success'){
            return response.data.data;
        }
        return null;
    }catch(error){
        console.error("logout failed")
    }
}