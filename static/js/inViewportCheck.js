function isElementInViewportBlock (el) {
    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
    );
}

function isElementInViewportInline (el) {
    var rect = el.getBoundingClientRect();

    return (
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

const weekdaysFixed = document.querySelector('.weekdays-fixed');
const hoursFixed = document.querySelector('.hours-fixed');
const weekdays = document.querySelector('.weekdays');
const hours = document.querySelector('.hours');
const hoursWidth = getComputedStyle(document.documentElement)
.getPropertyValue('--hours-width');
const mainWidth = parseInt(getComputedStyle(document.documentElement)
.getPropertyValue('--main-width'));


window.addEventListener('scroll', () => {
    if (!isElementInViewportBlock(weekdays)) {
        weekdaysFixed.style.display = 'flex';
        weekdays.style.visibility = 'hidden';
    } else {
        weekdaysFixed.style.display = 'none';
        weekdays.style.visibility = 'visible';
    }
})

let d = document.querySelector('.timetable-container');
d.addEventListener('scroll', () => {
    weekdaysFixed.style.left = `calc(${(100 - mainWidth)/2}vw + ${hoursWidth} - ${d.scrollLeft}px)`;
    //hoursFixed.style.left = `${d.scrollLeft}px`;
    if (d.scrollLeft > hours.style.width + 30) {
        hoursFixed.style.display = 'block';
        hours.style.visibility = 'hidden';
    } else {
        hoursFixed.style.display = 'none';
        hours.style.visibility = 'visible';
    }
});
    