// Checks if password length is 8 characters or more
export function checkLength(password){
    if(password.value.length >= 8){
        return true
    } else {
        return false
    }
}

export function checkLengthLonger(password){
    if(password.value.length >=12){
        return true
    } else {
        return false
    }
}

export function passwordCompare(password1, password2) {
    if(password1.value === password2.value && password2.value.length !== 0) {
        return true
    } else {
        return false
    }
}