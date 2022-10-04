const hamburger = document.querySelector('.menu-hamburger');
const nav = document.querySelector('nav');
const navSvg = document.querySelector('nav svg');

hamburger.addEventListener('click', () => {
    nav.style.right = 0;
});

navSvg.addEventListener('click', () => {
    nav.style.right = '-100%';
})