import axios from "axios"
import { BASE_URL } from "../config"

export const uploadFile = async(files: FileList) => {
    try{
        const formData = new FormData();
        for(let i=0; i< files.length; i++){
            formData.append("files", files[i])
        }
        const response = await axios.post(`${BASE_URL}/upload/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
        })
        console.log('response', response)
        if(response.data.data.status === 'Success'){
            return response.data;
        }
        return null;
    }catch(error){
        console.error("upload failed")
    }
}