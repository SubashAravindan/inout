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
    document.querySelector('body').append(img)
})

