import { decryptSecret, encryptSecretCredentials, encryptAdditionalData } from "./utilities/deriveKey.js";

const editForm = document.querySelector('#edit-account-form');
const usernameOrEmail = document.querySelector('#username-or-email');
const password = document.querySelector('#password');
const additionalData = document.querySelector('#additional-data');
const encryptedUsernameOrEmail = document.querySelector('[name="enc-username-or-email"]').value;
const usernameOrEmailIv = document.querySelector('[name="username-or-email-iv"]').value;
const encryptedPassword = document.querySelector('[name="enc-password"]').value;
const passwordIv = document.querySelector('[name="password-iv"]').value;
const encryptedAdditionalData = document.querySelector('[name="enc-additional-data"]').value;
const additionalDataIv = document.querySelector('[name="additional-data-iv"]').value;

const secretData = document.querySelector('[name="secret-data"]');


// Resets form if it is accessed from bfcache
window.addEventListener('pageshow', (e) => {
    if(e.persisted){
        editForm.reset();
    }
})

// listens for submit form then prompts user to enter master password to encrypt data
editForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    var data;
    var secretCredentials;
    var secretAdditionalData
    var masterPassword = prompt('Enter master password to confirm account edit: ')
    
    // Checks for changed username, password or no changes
    if(password.value.trim() && usernameOrEmail.value.trim()){
        secretCredentials = await encryptSecretCredentials(masterPassword.trim(), password.value.trim(), usernameOrEmail.value.trim())
    } else if(usernameOrEmail.value.trim()){
        secretCredentials = await encryptSecretCredentials(masterPassword.trim(), await decryptSecret(masterPassword, encryptedPassword, passwordIv), usernameOrEmail.value.trim())
    } else if(password.value.trim()) {
        secretCredentials = await encryptSecretCredentials(masterPassword.trim(), password.value.trim(), await decryptSecret(masterPassword, encryptedUsernameOrEmail, usernameOrEmailIv))
    } else if(!password.value.trim() && !usernameOrEmail.value.trim()) {
        secretCredentials = {}
    }

    // Checks for changed additional data
    if(additionalData.value.trim()){
        secretAdditionalData = await encryptAdditionalData(masterPassword.trim(), additionalData.value.trim());
    } else {
        secretAdditionalData = {};
    }

    
    if(!password.value.trim() && !usernameOrEmail.value.trim() && !additionalData.value.trim()) {
        alert("Can't save changes you didn't change anything!")
        
    } else {
        if(secretCredentials === null && secretAdditionalData === null){
            alert('Incorrect master password! Try again.')
        } else {
            data = {...secretCredentials, ...secretAdditionalData}
            secretData.value = JSON.stringify(data);

            // Clearing out data before submit so it won't reach server
            data = 'VariableFiller';
            usernameOrEmail.value = 'FieldFiller';
            password.value = 'FieldFiller';
            additionalData.value = 'FieldFiller';
            masterPassword = 'VariableFiller';
            secretAdditionalData = 'VariableFiller';
            secretCredentials = 'VariableFiller';
            editForm.submit();
        }
    }
})