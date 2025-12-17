import { checkLength, checkLengthLonger, passwordCompare } from "./utilities/checkPasswords.js"
import { initialKeyDerive } from "./utilities/deriveKey.js"

const registerForm = document.querySelector('#register-form')
const password1 = document.querySelector('#password1')
const password2 = document.querySelector('#password2')
const password1StatusSymbol = document.querySelector('#password1-status-symbol')
const password2StatusSymbol = document.querySelector('#password2-status-symbol')
const mPassword = document.querySelector('#m-password')
const mPassword2 = document.querySelector('#m-password2')
const mStatusSymbol = document.querySelector('#m-status-symbol')
const m2StatusSymbol = document.querySelector('#m2-status-symbol')
const registerBtn = document.querySelector('#register-btn')
const xUrl = registerForm.dataset.xImgUrl
const checkUrl = registerForm.dataset.checkImgUrl
var password1Valid
var password2Valid
var mPasswordValid 
var mPassword2Valid
var userPasswordCompare;
const inputFields = registerForm.querySelectorAll('input:not([type="hidden"])')
const profileData = document.querySelector('[name="profile-data"]');

// Processes master password then submits form
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    var data = await initialKeyDerive(mPassword.value);
    profileData.value = JSON.stringify(data);

    data = '';
    mPassword.value = '';
    mPassword2.value = '';

    registerForm.submit();
    
})


// Event listener to disable and enable register button 
registerForm.addEventListener('input', (e) => {


    password1Valid = checkLength(password1)

    if(password1Valid){
        password1StatusSymbol.src = checkUrl
    } else {
        password1StatusSymbol.src = xUrl
    }


    password2Valid = passwordCompare(password1, password2)

    if(password2Valid) {
        password2StatusSymbol.src = checkUrl
    } else {
        password2StatusSymbol.src = xUrl
    }
    

    mPasswordValid = checkLengthLonger(mPassword)
    userPasswordCompare = passwordCompare(mPassword, password1)

    if(mPasswordValid && !userPasswordCompare){
        mStatusSymbol.src = checkUrl
    } else {
        mStatusSymbol.src = xUrl
    }


    mPassword2Valid = passwordCompare(mPassword, mPassword2)
            
    if(mPassword2Valid) {
        m2StatusSymbol.src = checkUrl
    } else {
        m2StatusSymbol.src = xUrl
    }

    


    // switch (e.target) {
    //     // Checks length of password 1
    //     case password1:
    //         password1Valid = checkLength(e.target)

    //         if(password1Valid){
    //             password1StatusSymbol.src = checkUrl
    //         } else {
    //             password1StatusSymbol.src = xUrl
    //         }

    //     // Checks that password 1 and 2 match
    //     case password2:
            
    //         password2Valid = passwordCompare(password1, password2)

    //         if(password2Valid) {
    //             password2StatusSymbol.src = checkUrl
    //         } else {
    //             password2StatusSymbol.src = xUrl
    //         }
    //         break;

    //     // Checks length of master password
    //     case mPassword:
            
    //         mPasswordValid = checkLengthLonger(e.target)
    //         userPasswordCompare = passwordCompare(mPassword, password1)

    //         if(mPasswordValid){
    //             mStatusSymbol.src = checkUrl
    //         } else {
    //             mStatusSymbol.src = xUrl
    //         }

    //     // Checks that master password 1 and 2 match
    //     case mPassword2:
    //         mPassword2Valid = passwordCompare(mPassword, mPassword2)
            
    //         if(mPassword2Valid) {
    //             m2StatusSymbol.src = checkUrl
    //         } else {
    //             m2StatusSymbol.src = xUrl
    //         }
    //         break;    
    



    // Checks if all input fields are filled out
    var inputStatus = Array.from(inputFields).every(input => input.value.length >= 1)

    // Enables register button if all requirements are met and disables it if they are not
    if(password1Valid && password2Valid && mPasswordValid && mPassword2Valid && inputStatus){
        registerBtn.disabled = false
        registerBtn.style.opacity = "100%"
        registerBtn.classList.remove('disable-effects')
    } else {
        registerBtn.disabled = true
        registerBtn.style.opacity = "60%"
        registerBtn.classList.add('disable-effects')
        

    } 
})