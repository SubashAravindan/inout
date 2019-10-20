$('#newObjectForm #submit-button').click(e => {
    e.preventDefault()
    var data = new FormData()
    data.append('name',document.querySelector('#newObjectForm #text-input').value)
    data.append('description',document.querySelector('#newObjectForm #textarea-input').value)
    $.each($("#newObjectForm #file-multiple-input")[0].files, function(i, file) {
        data.append('file', file);
    });
    fetch('http:localhost:8897/new', {
        method: 'POST',
        body: data
    }).then(response => {
        if(response.status==200){
            window.location.href = 'objects.html?objectName=' + document.querySelector('#newObjectForm #text-input').value
        }
    })
})