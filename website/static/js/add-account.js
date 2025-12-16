import { encryptSecret } from "./utilities/deriveKey.js";

const newAccountForm = document.querySelector('#new-account-form')
const password = document.querySelector('#password')
const mPassword = document.querySelector('#m-password')
const usernameOrEmail = document.querySelector('#email-or-username')
const secretData = document.querySelector('[name="secret-data"]');

// Resets form if it is accessed from bfcache
window.addEventListener('pageshow', (e) => {
    if(e.persisted){
        newAccountForm.reset();
    }
})
// Submit event listener for new account form that prevents default
newAccountForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Getting master key then if successfull submitting form
    const data = await encryptSecret(mPassword.value.trim(), password.value.trim(), usernameOrEmail.value.trim())
    if(data === null){
        alert('Master key was incorrect encryption failed! Try again')
    } else {
        secretData.value = JSON.stringify(data)
        usernameOrEmail.value = 'FieldFiller'
        mPassword.value = 'FieldFiller'
        password.value = 'FieldFiller'
        newAccountForm.submit()
    }
    
        
    
})
