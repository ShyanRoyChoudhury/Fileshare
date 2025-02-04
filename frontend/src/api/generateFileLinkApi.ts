import axios from "axios"
import { BASE_URL } from "../config"

export const generateFileLinkApi = async(uid:string) => {
    try{
        const response = await axios.post(`${BASE_URL}/generateLink/${uid}/?permission=Write`, {}, {
            headers: {
                "Content-Type": "application/json",
                // "Cache-Control": "no-cache, no-store, must-revalidate",
            },
            withCredentials: true,
        })
        console.log('response in generate file api', response)
        if(response.data.status === 'Success'){
            return response.data;
        }
        return null;
    }catch(error){
        console.error("upload failed")
    }
}