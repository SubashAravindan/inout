const urlParams = new URLSearchParams(window.location.search);
const objectName = urlParams.get('objectName')

if(localStorage.getItem('inout') && JSON.parse(localStorage.getItem('inout'))[objectName]){
    let object = JSON.parse(localStorage.getItem('inout'))[objectName]
    let img = new Image()
    console.log('Cache hit for ' + object.name)
    img.src = 'data:image/jpeg;base64,' + object.image
    document.querySelector('.img-display').append(img)
    document.querySelector('.name-display').innerHTML = object.name
    document.querySelector('.description-display').innerHTML = object.description
}

fetch('http:localhost:8897?name=' + objectName, {
    method: 'GET',
    // mode:'no-cors',
}).then(response => response.text())
    .then(JSON.parse)
    .then(data => {
        let img = new Image()
        img.src = 'data:image/jpeg;base64,' + data[2]
        document.querySelector('.img-display').append(img)
        document.querySelector('.name-display').innerHTML = data[0]
        document.querySelector('.description-display').innerHTML = data[1]
        if(localStorage.getItem('inout')){
            localStorage.setItem('inout',JSON.stringify({...JSON.parse(localStorage.getItem('inout')),[data[0]]:{name:data[0],description:data[1],image:data[2]}}))
        }else{
            localStorage.setItem('inout',JSON.stringify({name:{name:data[0],description:data[1],image:data[2]}}))
        }
        // fetch('http:localhost:8897/new', {
        //     method: 'POST',
        //     body: JSON.stringify(data)
        // }).then(response=>response.json()).then(console.log)
    })

