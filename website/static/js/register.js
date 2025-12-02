const registerForm = document.querySelector('#register-form')
const password1 = document.querySelector('#password1')
const password2 = document.querySelector('#password2')
const password1StatusSymbol = document.querySelector('#password1-status-symbol')
const password2StatusSymbol = document.querySelector('#password2-status-symbol')
const registerBtn = document.querySelector('#register-btn')
const xUrl = registerForm.dataset.xImgUrl
const checkUrl = registerForm.dataset.checkImgUrl
var password1ValidStatus = false
var password2ValidStatus = false



// Event listener for checking password 1 length
password1.addEventListener('input', (e) => {
    
    if(e.target.value.length >= 8){
        password1StatusSymbol.src = checkUrl
        password1ValidStatus = true
    } else {
        password1StatusSymbol.src = xUrl
        password1ValidStatus = false
    }
    
})

// Event listener for compaing password 1 to password 2 to confirm matching
password2.addEventListener('input', (e) => {
    if(e.target.value === password1.value && e.target.value.length !== 0) {
        password2StatusSymbol.src = checkUrl
        password2ValidStatus = true
    } else {
        password2StatusSymbol.src = xUrl
        password2ValidStatus = false
    }
})

// Event listener to disable and enable register button 
registerForm.addEventListener('input', (e) => {
    if(password1ValidStatus && password2ValidStatus){
        registerBtn.disabled = false
        registerBtn.style.opacity = "100%"
    } else {
        registerBtn.disabled = true
        registerBtn.style.opacity = "60%"
    }
})