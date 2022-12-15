const adjustLine = (from, to, line) => {
    let fromTop = from.offsetTop + from.offsetHeight/2
    let toTop = to.offsetTop + to.offsetHeight/2
    let fromLeft = from.offsetLeft + from.offsetWidth/2
    let toLeft = to.offsetLeft + to.offsetWidth/2
    
    let horizontalDiff = Math.abs(toTop - fromTop)
    let verticalDiff = Math.abs(toLeft - fromLeft)
    let pitagoras = Math.sqrt(horizontalDiff*horizontalDiff + verticalDiff*verticalDiff)
    let angle = 180 / Math.PI * Math.acos( horizontalDiff/pitagoras )
  
    let top, left

    if(toTop > fromTop){
        top = (toTop-fromTop)/2 + fromTop
    }else{
        top = (fromTop-toTop)/2 + toTop
    }
    if(toLeft > fromLeft){
        left = (toLeft-fromLeft)/2 + fromLeft
    }else{
        left = (fromLeft-toLeft)/2 + toLeft
    }
  
    if((fromTop < toTop && fromLeft < toLeft) || (toTop < fromTop && toLeft < fromLeft) || (fromTop > toTop && fromLeft > toLeft) || (toTop > fromTop && toLeft > fromLeft)){
      angle *= -1
    }
    top -= pitagoras/2
  
    line.style["-webkit-transform"] = `rotate(${angle}deg)`
    line.style["-moz-transform"] = `rotate(${angle}deg)`
    line.style["-ms-transform"] = `rotate(${angle}deg)`
    line.style["-o-transform"] = `rotate(${angle}deg)`
    line.style["-transform"] = `rotate(${angle}deg)`
    line.style.top = top+'px'
    line.style.left = left+'px'
    line.style.height = pitagoras + 'px'
}

const cardContainer = document.querySelector('.card-container')
const cards = cardContainer.querySelectorAll('.card-single')

for (let i=0; i<cards.length-1; i++){
    let line = document.createElement('div')
    line.id = `card-line-${i}`
    line.classList.add('card-line')
    cardContainer.appendChild(line)
    adjustLine(cards[i], cards[i+1], line)
}