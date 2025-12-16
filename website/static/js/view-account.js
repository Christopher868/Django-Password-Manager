import { decryptSecret } from "./utilities/deriveKey.js";
const password = document.querySelector('#password');
const passwordIv = document.querySelector('#password-iv').textContent;
const usernameOrEmail = document.querySelector('#username-or-email');
const usernameOrEmailIv = document.querySelector('#username-or-email-iv').textContent;
const header = document.querySelector('#acc-info-header');

window.addEventListener('pageshow', (e)=> {
    if(e.persisted){
        header.innerHTML = "Refresh page"+ "<br>" +"to view info";
        usernameOrEmail.textContent = "null";
        password.textContent = "null"
    } else {
        decryptPassword() 
    }
    
});


// Calls decrypt function to decrypt encrypted password to be displayed
async function decryptPassword(){
    var masterPassword = prompt('Enter master password to decrypt saved account information.')
    if(masterPassword === null){
        alert('No password entered please refesh webpage and try again!')
    } else {
        var decryptedUsernameOrEmail = await decryptSecret(masterPassword, usernameOrEmail.textContent, usernameOrEmailIv)
        var decryptedPassword = await decryptSecret(masterPassword, password.textContent, passwordIv)
        if(decryptPassword === null || decryptedUsernameOrEmail === null){
            alert("Incorrect master key! Refresh page and try again.")
        } else {
            usernameOrEmail.textContent = decryptedUsernameOrEmail
            password.textContent = decryptedPassword
            decryptedUsernameOrEmail = null;
            decryptedPassword = null;
            masterPassword = null;
        }
    }
    
}


