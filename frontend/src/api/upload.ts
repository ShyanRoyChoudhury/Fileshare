import axios from "axios"
import { BASE_URL } from "../config"

export const uploadFile = async(files: FileList) => {
    try{
        // console.log('data:', data.length)
        // console.log('data:', data)
        const formData = new FormData();
        // files.forEach(file => {
        //     formData.append("files", file)
        // })
        // formData.append("files", files)
        for(let i=0; i< files.length; i++){
            formData.append("files", files[i])
        }
        const response = await axios.post(`${BASE_URL}/upload/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })
        console.log('response', response)
        if(response.data.status === 'Success'){
            return response.data;
        }
        return null;
    }catch(error){
        console.error("upload failed")
    }
}