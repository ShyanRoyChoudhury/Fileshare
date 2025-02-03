import axios from "axios"
import { BASE_URL } from "../config"

export const getProfileApi = async() => {
    try{
        const response = await axios.get(`${BASE_URL}/profile`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        if(response.data.data.status === 'Success'){
            console.log('response in get profiel api', response)
            return response.data.data;
        }
        return null;
    }catch(error){
        console.error("get profile api failed")
    }
}