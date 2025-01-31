import axios from "axios"
import { BASE_URL } from "../config"

export const getFileListApi = async() => {
    try{
        const response = await axios.get(`${BASE_URL}/getList`, {
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


// import axios from "axios";
// import { BASE_URL } from "../config";

// export const getFileListApi = async () => {
//     try {
//         const response = await axios.get(`${BASE_URL}/getList`, {
//             headers: {
//                 "Content-Type": "application/json",
//                 "Cache-Control": "no-cache", // Ensures fresh data
//             },
//             withCredentials: true,
//         });

//         if (response.data.status === "Success") {
//             return response.data;
//         }
//         return null;
//     } catch (error) {
//         console.error("API call failed", error);
//     }
// };
