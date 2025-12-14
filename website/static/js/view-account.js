import { decryptSecret } from "./utilities/deriveKey.js";
const masterPassword = prompt('Enter master password to decrypt saved info')
const password = document.querySelector('#password');
const savedIv = document.querySelector('#iv').textContent;

// Calls decrypt function to decrypt encrypted password to be displayed
async function decryptPassword(){
    const result = await decryptSecret(masterPassword, password.textContent, savedIv)
    if(result === null){
        alert("Incorrect master key! Refresh page and try again.")
    } else {
        password.textContent = result
    }
}

decryptPassword()