import axios from "axios"
import { BASE_URL } from "../config"

export const deleteFileApi = async(uid:string) => {
    try{
        const response = await axios.get(`${BASE_URL}/delete/${uid}`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        console.log('response in delete file api', response)
        if(response.data.status === 'Success'){
            return response.data;
        }
        return null;
    }catch(error){
        console.error("upload failed")
    }
}