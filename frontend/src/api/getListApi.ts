import axios from "axios"
import { BASE_URL } from "../config"

export const getFileListApi = async() => {
    try{
        const response = await axios.post(`${BASE_URL}/getList`, {} ,{
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        console.log('response in get file api', response)
        if(response.data.data.status === 'Success'){
            return response.data.data;
        }
        return null;
    }catch(error){
        console.error("upload failed")
    }
}