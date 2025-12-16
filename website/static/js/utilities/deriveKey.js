import { enc, dec, arrayBufferToBase64, base64ToArrayBuffer} from './conversionHelper.js'
import { getStoredProfileData } from './fetchData.js';

// Generates encrypted validation text using the master password used at account creation for validation later
export async function initialKeyDerive(masterPassword){
    const salt = window.crypto.getRandomValues(new Uint8Array(16));

    const iterations = 500000;
    const keyLength = 256;
    
    const passwordKey = await window.crypto.subtle.importKey(
        'raw',
        enc.encode(masterPassword),
        { name: 'PBKDF2'},
        false,
        ['deriveKey']
    );


    const derivedKey = await window.crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt, 
            iterations: iterations,
            hash: 'SHA-256'
        },
        passwordKey,
        { name: 'AES-GCM', length: keyLength },
        false,
        ['encrypt', 'decrypt']
    );

    const validationText = window.crypto.getRandomValues(new Uint8Array(32));
    const validationIV = window.crypto.getRandomValues(new Uint8Array(12));
    

    const encryptedValidationText = await window.crypto.subtle.encrypt(
        { name: 'AES-GCM', iv: validationIV },
        derivedKey,
        validationText
    );

    return {
        salt: arrayBufferToBase64(salt.buffer),
        iterations: iterations,
        validation_ciphertext: arrayBufferToBase64(encryptedValidationText),
        validation_iv: arrayBufferToBase64(validationIV.buffer)
    }


}

// Recreates master key using input masterpassword and stored key components from db
export async function deriveKeyFromStorage(masterPassword, storedKeyComponents){
    const salt = base64ToArrayBuffer(storedKeyComponents.salt);
    const iterations = storedKeyComponents.iterations

    const passwordKey = await window.crypto.subtle. importKey(
        'raw',
        enc.encode(masterPassword),
        { name: 'PBKDF2' },
        false, 
        ['deriveKey']
    );


    const derivedKey = await window.crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,
            iterations: iterations,
            hash: 'SHA-256'
        },
        passwordKey,
        { name: 'AES-GCM', length: 256},
        false, 
        ['encrypt', 'decrypt']
    );

    return derivedKey;
}


// Verifies that the user's master password is correct
async function verifyMasterPassword(masterPassword){
    const storedKeyComponents = await getStoredProfileData();
    const derivedKey = await deriveKeyFromStorage(masterPassword, storedKeyComponents);

    const ciphertext = base64ToArrayBuffer(storedKeyComponents.cipher_text);
    const iv = base64ToArrayBuffer(storedKeyComponents.iv);

    try{
        const decryptedValidationText = await window.crypto.subtle.decrypt(
        { name: 'AES-GCM', iv:iv },
        derivedKey,
        ciphertext
        );
        return derivedKey
    } catch (err){
        console.error(`Incorrect master password: ${err}`);
        return null;
    }
}


// Encrypts data before being sent to database
export async function encryptSecret(masterPassword, secretPassword, secretUsernameOrEmail){
    const derivedMasterKey = await verifyMasterPassword(masterPassword)
    if(derivedMasterKey === null){
        return null;
    } else {
        const iv = window.crypto.getRandomValues(new Uint8Array(12));

        const encryptedPassword = await window.crypto.subtle.encrypt(
            { name: 'AES-GCM', iv: iv },
            derivedMasterKey,
            enc.encode(secretPassword)
        );

         const encryptedUsernameOrEmail = await window.crypto.subtle.encrypt(
            { name: 'AES-GCM', iv: iv },
            derivedMasterKey,
            enc.encode(secretUsernameOrEmail)
        );

        return {
            enc_password: arrayBufferToBase64(encryptedPassword),
            enc_username_or_email: arrayBufferToBase64(encryptedUsernameOrEmail),
            validation_iv: arrayBufferToBase64(iv.buffer)
        }
    }
}


// Decrypts password for user to view then returns it
export async function decryptSecret(masterPassword, secret, iv){
    
    iv = base64ToArrayBuffer(iv)
    const encryptedSecret = base64ToArrayBuffer(secret)
    const derivedMasterKey = await verifyMasterPassword(masterPassword)

    try{
        const plaintextBuffer = await window.crypto.subtle.decrypt(
            { name: 'AES-GCM', iv:iv },
            derivedMasterKey,
            encryptedSecret
        );

        return dec.decode(plaintextBuffer)

    } catch (err) {
        console.error("Decryption failed:", err)
        return null;
    }
}






