import { encryptSecret, decryptSecret } from "./utilities/deriveKey.js";

const editForm = document.querySelector('#edit-account-form');
const usernameOrEmail = document.querySelector('#username-or-email');
const password = document.querySelector('#password')
const encryptedUsernameOrEmail = document.querySelector('[name="enc-username-or-email"]').value;
const usernameOrEmailIv = document.querySelector('[name="username-or-email-iv"]').value;
const encryptedPassword = document.querySelector('[name="enc-password"]').value;
const passwordIv = document.querySelector('[name="password-iv"]').value;
const secretData = document.querySelector('[name="secret-data"]');



editForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    var data;
    var masterPassword = prompt('Enter master password to confirm account edit: ')
    
    // Only changes changed field and does not allow spaces
    if(password.value.trim() && usernameOrEmail.value.trim()){
        data = await encryptSecret(masterPassword.trim(), password.value.trim(), usernameOrEmail.value.trim())
    } else if(usernameOrEmail.value.trim()){
        data = await encryptSecret(masterPassword.trim(), await decryptSecret(masterPassword, encryptedPassword, passwordIv), usernameOrEmail.value.trim())
    } else if(password.value.trim()) {
        data = await encryptSecret(masterPassword.trim(), password.value.trim(), await decryptSecret(masterPassword, encryptedUsernameOrEmail, usernameOrEmailIv))
    } else {
        alert("Nothing saved no changes were made!")
    }
     
    if(data === null){
        alert('Incorrect master password! Try again.')
    } else {
        secretData.value = JSON.stringify(data);
        data = 'VariableFiller';
        usernameOrEmail.value = 'FieldFiller';
        password.value = 'FieldFiller';
        masterPassword = 'VariableFiller';
        editForm.submit();
        
    }
})