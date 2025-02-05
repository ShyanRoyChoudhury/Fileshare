import axios from "axios"
import { BASE_URL } from "../config"
import { toast } from "react-toastify"

export const deleteFileApi = async(uid:string) => {
    try{
        const response = await axios.get(`${BASE_URL}/delete/${uid}`, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        })
        console.log('response in delete file api', response)
        if(response?.data?.data?.status === 'Success'){
            toast.success("File Deleted Successfully")
            return response.data;
        }
        toast.error("File Delete Unsuccessfull")
        return null;
    }catch(error){
        toast.error("File Delete Unsuccessfull")
    }
}