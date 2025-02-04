export const deriveKey = async (password: string, salt: BufferSource) => {
    const encoder = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
      "raw",
      encoder.encode(password),
      { name: "PBKDF2" },
      false,
      ["deriveKey"]
    );
  
    return crypto.subtle.deriveKey(
      {
        name: "PBKDF2",
        salt: salt,
        iterations: 100000, // High iteration count for security
        hash: "SHA-256",
      },
      keyMaterial,
      { name: "AES-GCM", length: 256 }, // AES-256 key
      true, // Key is not extractable
      ["encrypt", "decrypt"] // Key usage
    );
};