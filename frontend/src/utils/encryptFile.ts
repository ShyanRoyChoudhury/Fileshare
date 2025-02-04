import { deriveKey } from "./deriveKey";

export const encryptFile = async (file: File, password: string) => {
    const salt = crypto.getRandomValues(new Uint8Array(16)); // 16-byte salt
    const iv = crypto.getRandomValues(new Uint8Array(12)); // 12-byte IV for AES-GCM
    const key = await deriveKey(password, salt);
  
    const fileData = await file.arrayBuffer();
    const ciphertext = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      key,
      fileData
    );
    console.log('key', key)
    // Combine IV, salt, and ciphertext into a single Blob
    const encryptedBlob = new Blob([iv, salt, new Uint8Array(ciphertext)], {
      type: "application/octet-stream",
    });
  
    return {encryptedBlob, key };
  };