export const enc = new TextEncoder();
export const dec = new TextDecoder();

export function base64ToArrayBuffer(base64String) {
    const binaryString = atob(base64String);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    
    return bytes;
}

export function arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    
    bytes.forEach(byte => {
        binary += String.fromCharCode(byte);
    });
    
    return btoa(binary);
}