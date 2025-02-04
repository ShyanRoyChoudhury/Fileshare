import { deriveKey } from "./deriveKey";

export const decryptFile = async (encryptedBlob: Blob, password: string) => {
    const encryptedData = await encryptedBlob.arrayBuffer();
  
    // Extract IV (first 12 bytes), salt (next 16 bytes), and ciphertext (rest)
    const iv = encryptedData.slice(0, 12);
    const salt = encryptedData.slice(12, 28);
    const ciphertext = encryptedData.slice(28);
  
    const key = await deriveKey(password, new Uint8Array(salt));
    console.log("key", key)
    console.log("cipherText", ciphertext)
    console.log("salt", salt)
    
    const decryptedData = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: new Uint8Array(iv) },
      key,
      ciphertext
    );
  
    return new Blob([decryptedData], { type: "application/octet-stream" });
  };