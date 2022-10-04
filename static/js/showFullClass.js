const classes = document.querySelectorAll('.plan-single');

classes.forEach((el) => {
    el.addEventListener('click', () => {
        classes.forEach((e) => {
            if (e==el) e.classList.toggle('plan-full');
            else e.classList.remove('plan-full');
        })
    })
})