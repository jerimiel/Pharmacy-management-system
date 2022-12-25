const addEl = document.getElementById("add-el")
const removeEl = document.getElementById("remove-el")
const searchEl = document.getElementById("search-el")
const deleteAllEl = document.getElementById("deleteall-el")
const nameEl = document.getElementById("title-el")
const brandEl = document.getElementById("brand-el")
const dateEl = document.getElementById("date-el")
const priceEl = document.getElementById("price-el")
const warnings = document.getElementById("warnings")
const qtyEl = document.getElementById("qty-el")
const updateEl = document.getElementById("update-el")
let details = {}


fetch(`/getall`)
    .then(response => response.json())  
    .then(json => {
        //let data = JSON.stringify(json)
        let rows = ''
        for(let i=0;i<json.length;i+=1){
            let data = json[i]
            let cells = ''
            for(let j=0;j<data.length;j+=1){
                cells = cells + `<td>${data[j]}</td>`
            }
            rows = rows + `<tr>`+cells+`</tr>`
        }
        document.getElementById("demo").innerHTML = `<table id="database"> <caption id="table-cap">Database</caption> <tr><th>Name</th><th>Brand</th><th>Exp date</th><th>price</th><th>Qty</th></tr>`+rows+`</table>`
    })


addEl.addEventListener("click",function(){
    warnings.innerHTML = ""
    details['name'] = nameEl.value
    details['brand'] = brandEl.value
    details['date'] = dateEl.value
    details['price'] = priceEl.value
    details['quantity'] = qtyEl.value
    if((Number(priceEl.value) === NaN) || (priceEl.value === '')){
        details['price'] = 0.00
    }
    if((nameEl.value === '')||(brandEl.value === '')){
        warnings.innerHTML = "Title and brand can't be empty"
    }
    else{
    fetch(`/sendinfo/${JSON.stringify(details)}`)
    .then(response => response.json())  
    .then(json => {
        //let data = JSON.stringify(json)
        let rows = ''
        for(let i=0;i<json.length;i+=1){
            let data = json[i]
            let cells = ''
            for(let j=0;j<data.length;j+=1){
                cells = cells + `<td>${data[j]}</td>`
            }
            rows = rows + `<tr>`+cells+`</tr>`
        }
        document.getElementById("demo").innerHTML = `<table id="database"> <caption id="table-cap">Database</caption> <tr><th>Name</th><th>Brand</th><th>Exp date</th><th>price</th><th>Qty</th></tr>`+rows+`</table>`
    })
    }
})

removeEl.addEventListener("click",function(){
    warnings.innerHTML = ""
    details['name'] = nameEl.value
    details['brand'] = brandEl.value
    if((details['name'] === '') || (details['brand'] === '')){
        warnings.innerHTML = "You will need both the title and brand of drug to remove one"
    }
    else{
        const request = new XMLHttpRequest()
        request.open('POST',`/removeinfo/${JSON.stringify(details)}`)
        request.send();
        fetch(`/removeinfo/${JSON.stringify(details)}`)
        .then(response => response.json())  
        .then(json => {
        console.log(json)
        let data = JSON.stringify(json)
        document.getElementById("demo").innerHTML = data
    })
    }
})

searchEl.addEventListener("click",function(){
    //beginning of function
    warnings.innerHTML = ""
    details['name'] = nameEl.value
    details['brand'] = brandEl.value
    console.log(details)
    if((details['name'] === '') || (details['brand'] === '')){
        warnings.innerHTML = "You will need both the title and brand of drug to search for one"
    }
    else{
        const request = new XMLHttpRequest()
        request.open('POST',`/searchinfo/${JSON.stringify(details)}`)
        request.send();
        fetch(`/searchinfo/${JSON.stringify(details)}`)
       .then(response => response.json())  
       .then(json => {
        //let data = JSON.stringify(json)
        let rows = ''
        for(let i=0;i<json.length;i+=1){
            let data = json[i]
            let cells = ''
            for(let j=0;j<data.length;j+=1){
                cells = cells + `<td>${data[j]}</td>`
            }
            rows = rows + `<tr>`+cells+`</tr>`
        }
        document.getElementById("demo").innerHTML = `<table id="database"> <caption id="table-cap">Search results</caption> <tr><th>Name</th><th>Brand</th><th>Exp date</th><th>price</th><th>Qty</th></tr>`+rows+`</table>`
    })
    }
    //end of function
})

deleteAllEl.addEventListener("click",function(){
    if(confirm("Are you sure you want to delete all entries?")){
        const request = new XMLHttpRequest()
        request.open('POST',`/deleteall`)
        request.send();
        document.getElementById("demo").innerHTML = `<table id="database"> <caption id="table-cap">Updated entry</caption> <tr><th>Name</th><th>Brand</th><th>Exp date</th><th>price</th><th>Qty</th></tr></table>`
    }
})

updateEl.addEventListener("click",function(){
    warnings.innerHTML = ""
    details['name'] = nameEl.value
    details['brand'] = brandEl.value
    details['date'] = dateEl.value
    details['price'] = priceEl.value
    details['quantity'] = qtyEl.value
    if((nameEl.value === '') || (brandEl.value === '')){warnings.innerHTML = "title and brand can't be empty"}
    else{
        fetch(`/updateinfo/${JSON.stringify(details)}`)
       .then(response => response.json())  
       .then(json => {
        let rows = ''
        //let data = JSON.stringify(json)
        for(let i=0;i<json.length;i+=1){
            let data = json[i]
            let cells = ''
            for(let j=0;j<data.length;j+=1){
                cells = cells + `<td>${data[j]}</td>`
            }
            rows = rows + `<tr>`+cells+`</tr>`
        }
        document.getElementById("demo").innerHTML = `<table id="database"> <caption id="table-cap">Updated entry</caption> <tr><th>Name</th><th>Brand</th><th>Exp date</th><th>price</th><th>Qty</th></tr>`+rows+`</table>`
        
    })

    }
})
