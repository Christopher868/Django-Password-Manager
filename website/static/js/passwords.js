const searchBar = document.querySelector('#search')
const accountPasswords = document.querySelectorAll('.pwd')


// Filters passwords using search bar input
searchBar.addEventListener('input', (e) => {
    const input = e.target.value.toLowerCase();

    accountPasswords.forEach(account => {
        const accountName = account.querySelector('h4').textContent.toLowerCase()

        if(accountName.includes(input) || input === ''){
            account.classList.remove('fast-hidden')
        } else {
            account.classList.add('fast-hidden')
        }
    })
})