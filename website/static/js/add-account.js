const newAccountForm = document.querySelector('#new-account-form')

// Submit event listener for new account form that prevents default
newAccountForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Getting form data
    const formData = new FormData(newAccountForm)
    const accountTitle = formData.get('account-title')
    const emailOrUsername = formData.get('email-or-username')
    const password = formData.get('password')
    
    
})