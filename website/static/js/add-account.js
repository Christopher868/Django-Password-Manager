import { encryptSecret } from "./utilities/deriveKey.js";

const newAccountForm = document.querySelector('#new-account-form')
const password = document.querySelector('#password')
const mPassword = document.querySelector('#m-password')
const secretData = document.querySelector('[name="secret-data"]');
// Submit event listener for new account form that prevents default
newAccountForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Getting master key then if successfull submitting form
    const data = await encryptSecret(mPassword.value, password.value)
    if(data === null){
        alert('Master key was incorrect encryption failed! Try again')
    } else {
        secretData.value = JSON.stringify(data)
        mPassword.value = 'FieldFiller'
        password.value = 'FieldFiller'
        newAccountForm.submit()
    }
    
        
    
})
