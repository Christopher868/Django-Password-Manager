import { decryptSecret } from "./utilities/deriveKey.js";
const password = document.querySelector('#password');
const savedIv = document.querySelector('#iv').textContent;
const usernameOrEmail = document.querySelector('#username-or-email')

// Calls decrypt function to decrypt encrypted password to be displayed
async function decryptPassword(){
    const masterPassword = prompt('Enter master password to decrypt saved account information.')
    const decryptedUsernameOrEmail = await decryptSecret(masterPassword, usernameOrEmail.textContent, savedIv)
    const decryptedPassword = await decryptSecret(masterPassword, password.textContent, savedIv)
    if(decryptPassword === null || decryptedUsernameOrEmail === null){
        alert("Incorrect master key! Refresh page and try again.")
    } else {
        usernameOrEmail.textContent = decryptedUsernameOrEmail
        password.textContent = decryptedPassword
    }
}

decryptPassword()