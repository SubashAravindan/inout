const config = {
    canvas: {
        height: 1000,
        width: 1000
    },
    serverURL: 'ws://127.0.0.1:8765'
}
console.log("hi")
const canvas = document.createElement('canvas')
canvas.height = config.canvas.height
canvas.width = config.canvas.width
document.getElementById('canvasContainer').append(canvas)
let ctx = canvas.getContext('2d')
let target_label = "all";

// ctx.fillStyle = 'red'
ctx.clearRect(0, 0, canvas.width, canvas.height)

function drawOneBox(prediction) {
    // console.log(prediction);

    let x1 = prediction.topleft.x;
    let y1 = prediction.topleft.y;
    let x2 = prediction.bottomright.x;
    let y2 = prediction.bottomright.y;
    ctx.beginPath();
    ctx.strokeStyle = "white";
    ctx.lineWidth = Number(prediction.confidence / 10);
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
    // console.log(x1, y1, x2 - x1, y2 - y1);
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(prediction.label, (x1 + x2) / 2, y1 - 20);
}

function DrawBoxes(predictions) {
    // console.log("lol")
    let allLabels = true;
    if (target_label !== "all") {
        allLabels = false;
    }
    for (let i = 0; i < predictions.length; ++i) {
        if (predictions[i].label === target_label) {
            drawOneBox(predictions[i]);
        }
        else if (allLabels) {
            drawOneBox(predictions[i]);
        }
    }
}

function drawImage(blob, predictions) {
    let img = new Image()
    img.onload = function () {
        ctx.drawImage(img, 0, 0)
        DrawBoxes(predictions)

    }
    img.src = blob
    // console.log(img.src);
}

const socket = new WebSocket(config.serverURL)

socket.onopen = (e) => {
    console.log('connection established')
    socket.send("Hello server!");

}

socket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    console.log('​socket.onmessage -> e', data)
    drawImage(('data:image/jpeg;base64,' + data.image), data.result)
}

socket.onclose = (e) => {
    console.log('closed')
}


function showObjectDetails(object) {
    window.location.href = "objects.html?objectName=" + object;
}
