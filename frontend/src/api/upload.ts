import axios from "axios"
import { BASE_URL } from "../config"


export const uploadFile = async({files, password}: {
    files: Blob;
    password: string;
}) => {
    try {
        // const exportedKey = await crypto.subtle.exportKey('jwk', key);

        const formData = new FormData();
        formData.append("files", files);
        formData.append("password", password);

        // Send base64 encoded salt and IV
        // formData.append("salt", base64EncodeArrayBuffer(salt));
        // formData.append("iv", base64EncodeArrayBuffer(iv));

        const response = await axios.post(`${BASE_URL}/upload/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
        })

        if(response.data?.data?.status === 'Success'){
            return response.data;
        }
        return null;
    } catch(error) {
        console.error("upload failed", error)
        return null;
    }
}