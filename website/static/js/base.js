const sidebar = document.querySelector('#base-sidebar')
const menuBtn = document.querySelector('#menu-btn')


// document event listener for clicks
document.addEventListener('click', (e) => {
    console.log(e.target.closest('li'))
    if(e.target.closest('li') === menuBtn) {
       sidebar.classList.toggle('hidden');
    }
})