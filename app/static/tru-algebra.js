let alg = 0;
let op = '';
let neg = '';
let varX = '';
const algL = document.querySelector('#algL')
const algR = document.querySelector('#algR')
let my_equation = document.getElementById('equation')


numButs = document.querySelectorAll(".nums")

function alsoR() {
    algR.textContent = algL.textContent
}

for (let i=0; i<numButs.length; i++) {
    numButs[i].addEventListener('click', (event) => {
        if (op && Math.log10(alg) <= 4 && !varX) {
            alg = alg * 10 + parseInt(event.target.textContent)
            algL.textContent = `${op}${neg}${alg}`
            alsoR()
        }
    })
}

opButs = document.querySelectorAll(".ops")

for (let i=0; i<opButs.length; i++) {
    opButs[i].addEventListener('click', (event) => {
        op = event.target.textContent
        alg = 0
        neg = ''
        algL.textContent = `${op}`
        alsoR()
    })
}

delBut = document.getElementById('del')

delBut.addEventListener('click', () => {
    if (!op) {
        //do nothing
    } else if (!neg && alg === 0) { //this deletes the operation
        algL.textContent = ""
        op = ''
    } else if (neg && alg === 0) { //this deletes the negative symbol
        algL.textContent = op;
        neg = '';
    } else if (!!varX) { //this deletes the variable
        varX = ''
        algL.textContent = `${op}${neg}${alg}`
    } else {
        alg = (alg - alg%10) / 10
        if (alg === 0) {
            algL.textContent = `${op}${neg}`
        } else {
            algL.textContent = `${op}${neg}${alg}`
        } 
    }
    alsoR()
})

negBut = document.getElementById('neg')

negBut.addEventListener('click', () => {
    if (op) {
        neg = neg ? '' : '-'
        if (alg) {
            algL.textContent = `${op}${neg}${alg}${varX}`
        } else {
            algL.textContent = `${op}${neg}${varX}`
        }
        alsoR()
    }
    
})

solved = function() {
    if (this.readyState == 4 && this.status == 200) {
        result = eval(this.response)
        if (result) {
            document.getElementById('middle').remove()
            document.getElementById('all_buttons').remove()
            simpButs = document.querySelectorAll('.simp')
            for (i=0; i<simpButs.length; i++) simpButs[i].remove()
            document.getElementById('endBox').hidden = false
        }
    }
}


checkSolution = function() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = solved
    xhttp.open("GET", '/equations/check_solution', true)
    xhttp.send()
}

ajaxOnComplete = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(this.response)
        equation = eval(this.response)
        my_equation.textContent = `$$${equation[0]}=${equation[1]}$$`
        MathJax.typeset()
        checkSolution()
    }
}

distButs = document.querySelectorAll('.distribute')

for (let i=0; i<distButs.length; i++) {
    distButs[i].addEventListener('click', (event) => {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = ajaxOnComplete
        xhttp.open("GET", `/equations/distribute/${event.target.id}`, true)
        clearHints()
        xhttp.send()
    })
}

combButs = document.querySelectorAll('.combine')

for (let i=0; i<combButs.length; i++) {
    combButs[i].addEventListener('click', (event) => {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = ajaxOnComplete
        xhttp.open("GET", `/equations/combine/${event.target.id}`, true)
        clearHints()
        xhttp.send()
    })
}

swapBut = document.getElementById('swap')

swapBut.addEventListener('click', () => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = ajaxOnComplete
    xhttp.open("GET", "/equations/swap", true)
    clearHints()
    xhttp.send()
})

varBut = document.getElementById("var")

varBut.addEventListener('click', () => {
    if (op) {
        varX = !!varX ? '' : 'x'
        algL.textContent = !!alg ? `${op}${neg}${alg}${varX}` : `${op}${neg}${varX}`
        alsoR()
    }
})

undoBut = document.getElementById('undo')

undoBut.addEventListener('click', () => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = ajaxOnComplete
    xhttp.open("GET", "/equations/undo", true)
    clearHints()
    xhttp.send()
})

enterBut = document.getElementById('enter')

enterBut.addEventListener('click', () => {
    if (op && (alg || varX)) {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = ajaxOnComplete
        message = algL.textContent
        if (message[0] === '+' || message[0] === '-') {
            xhttp.open("GET", `/equations/add_sub?alg=${message}`)
        }
        else if (message[0] === '×') {
            xhttp.open("GET", `/equations/multi?alg=${message.slice(1)}`)
        }
        else if (message[0] === '÷') {
            xhttp.open("GET", `/equations/div?alg=${message.slice(1)}`)
        }
        op = ''
        alg = 0
        neg = ''
        varX = ''
        algL.textContent = ''
        alsoR()
        clearHints()
        xhttp.send()
    }
})

function clearHints() {
    document.querySelectorAll('.hintColor').forEach(elem => {
        elem.classList.remove('hintColor')
    })
}

hintBut = document.getElementById('hint')

gimmeTheHint = function() {
    if (this.readyState == 4 && this.status == 200) {
        hint = eval(this.response)
        if (hint == "mul") {
            hint = "×"
        } else if (hint == "div") {
            hint = "÷"
        } 
        if (hint) {
            for (let i=0; i<hint.length; i++) {
                document.getElementById(hint[i]).classList.add('hintColor')
                
            }
        }
    }
}

hintBut.addEventListener('click', () => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = gimmeTheHint
    xhttp.open("GET", "/equations/hint", true)
    xhttp.send()
})