const sidebar = document.querySelector('#base-sidebar')
const menuBtn = document.querySelector('#menu-btn')
const closeBtn = document.querySelector('#close-btn')
const messageContainer = document.querySelector('#message-container')
const messages = document.querySelectorAll('.message')



// document event listener for clicks
document.addEventListener('click', (e) => {
    
    // if statement for opening and closing sidebar\
    if(sidebar){
        if(e.target.closest('li') === menuBtn) {
        sidebar.classList.toggle('smooth-hidden');
        } else if(e.target.closest('div') !== sidebar || e.target.closest('li') === closeBtn ){
            sidebar.classList.add('smooth-hidden');
        }
    }
})

// Timeout to make messages start to fade after 3 seconds and disappear after 6 seconds
if(messages){
    setTimeout(() => {
        messages.forEach(message => {
            message.classList.add('fade')
        })
        setTimeout(() => {
        if(messageContainer){
            messageContainer.classList.add('fast-hidden')
        }
        },3000)
    },4000)
}
