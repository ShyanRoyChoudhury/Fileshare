export function base64EncodeArrayBuffer(buffer: Uint8Array): string {
    return btoa(
        Array.from(buffer, byte => String.fromCharCode(byte)).join('')
    );
}