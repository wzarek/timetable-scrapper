const menu = document.querySelector('[data-menu-options]')

menu.addEventListener('click', () => {
    menu.classList.toggle('menu-shown')
})