// get csrf_token value
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');

let headers = new Headers({
    'Content-Type': 'text/json',
    'X-CSRFToken': csrftoken,
});

$("#test").click(function () {
    fetch('csrftokentest', {
        method: 'post',
        headers: headers,
        body: JSON.stringify({
            contents: $("#contents").val(),
        })
    }).then(response => response.json())
        .then(data => {
            alert(data.data)
        })
})
