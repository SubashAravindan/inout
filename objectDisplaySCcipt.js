const urlParams = new URLSearchParams(window.location.search);
const objectName = urlParams.get('objectName')

console.log(objectName)

let scriptFiles = document.querySelectorAll('script')
// console.log($.csv.toArray((scriptFiles[scriptFiles.length-1].src.replace('objectDisplaySCcipt.js','data,csv'))));
var reader = new FileReader();
console.log(scriptFiles[scriptFiles.length-1].src.replace('objectDisplaySCcipt.js','data.csv').slice(7));

reader.readAsText(scriptFiles[scriptFiles.length-1].src.replace('objectDisplaySCcipt.js','data.csv').slice(7));
reader.onload = function (event) {
    var csv = event.target.result;
    var data = $.csv.toArrays(csv);
    $('#result').empty();
    $('#result').html(JSON.stringify(data, null, 2));
}
