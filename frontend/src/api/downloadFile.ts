import axios from "axios";
import { BASE_URL } from "../config";
import { decryptFile } from "../utils/decryptFile";

export const downloadFileApi = async (uid: string) => {
    try {
        const response = await axios.get(`${BASE_URL}/download/${uid}`, {
            responseType: "blob",  // Ensure binary data handling
            withCredentials: true,
        });

        const encrptedData = response.data;
        const decryptedBlob = await decryptFile(encrptedData, "test123")

        // Extract filename from Content-Disposition header
        const contentDisposition = response.headers["content-disposition"];
        let filename = "downloaded-file"; // Default filename
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="(.+?)"/);
            if (match && match[1]) {
                filename = match[1];
            }
        }

        // Infer file extension from MIME type if filename doesn't have an extension
        const mimeType = response.headers["content-type"];
        const extensionMap: { [key: string]: string } = {
            "application/pdf": ".pdf",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "application/zip": ".zip",
            "text/csv": ".csv",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        };

        if (!filename.includes(".") && mimeType && extensionMap[mimeType]) {
            filename += extensionMap[mimeType];
        }

        // Create a Blob and trigger the file download
        // const url = window.URL.createObjectURL(new Blob([response.data], { type: mimeType }));
        const url = window.URL.createObjectURL(decryptedBlob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();

        // Cleanup
        link.remove();
        window.URL.revokeObjectURL(url);

        return true;
    } catch (error) {
        console.error("Download failed", error);
        return false;
    }
};
