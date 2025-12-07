const accountNames = document.querySelectorAll('.account') 
const searchBar = document.querySelector('#account-search')


// Filters accounts with search bar input value
searchBar.addEventListener('input', (e) => {
    accountNames.forEach(accountName => {
        if(!accountName.textContent.toLowerCase().includes(e.target.value.toLowerCase())){
            accountName.classList.add('fast-hidden')
        } else {
            accountName.classList.remove('fast-hidden')
        }
    })
})