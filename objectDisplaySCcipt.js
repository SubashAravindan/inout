const urlParams = new URLSearchParams(window.location.search);
const objectName = urlParams.get('objectName')

fetch('http:localhost:8897?name=' + objectName, {
    method: 'GET',
    // mode:'no-cors',
}).then(response => response.text())
.then(JSON.parse)
.then(data => {
    let img = new Image()
    img.src = 'data:image/jpeg;base64,' + data[2]
    document.querySelector('.img-display').append(img)
    document.querySelector('.name-display').innerHTML=data[0]
    document.querySelector('.description-display').innerHTML=data[1]
})

