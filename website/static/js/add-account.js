import { encryptSecretCredentials, encryptAdditionalData } from "./utilities/deriveKey.js";

const newAccountForm = document.querySelector('#new-account-form');
const password = document.querySelector('#password');
const mPassword = document.querySelector('#m-password');
const usernameOrEmail = document.querySelector('#email-or-username');
const additionalData = document.querySelector('#additional-data');
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
    var data;
    // Getting master key then if successfull submitting form
    if(!password.value && !usernameOrEmail.value){
        alert('Atleast 1 of "username or email" or "password" me be filled out!');
    } else {
        if(!password.value) {
            password.value = 'Blank';
        } else if(!usernameOrEmail.value){
            usernameOrEmail.value = 'Blank';
        } else if (!additionalData.value){
            additionalData.value = 'Blank';
        }
        var secretCredentials = await encryptSecretCredentials(mPassword.value.trim(), password.value.trim(), usernameOrEmail.value.trim());
        var secretAdditionalData = await encryptAdditionalData(mPassword.value.trim(), additionalData.value);
        if(secretCredentials === null || secretAdditionalData === null){
            alert('Master key was incorrect encryption failed! Try again');
        } else {
            data = { ...secretCredentials, ...secretAdditionalData};
            secretData.value = JSON.stringify(data);

            // Wiping data variables before sumbitting
            usernameOrEmail.value = 'FieldFiller';
            mPassword.value = 'FieldFiller';
            password.value = 'FieldFiller';
            additionalData.value = 'FieldFiller'
            data = 'VariableFiller';
            secretCredentials = 'VariableFiller'
            secretAdditionalData = 'VariableFiller'
            newAccountForm.submit();
        }
    }
    
    
        
    
})
