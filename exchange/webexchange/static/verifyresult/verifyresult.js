
    window.onload = () => {
        const csrftoken = getCookie('csrftoken');
        if (csrftoken == "") {
            csrftoken = None;
        }
        const requestData = {
            dataRequest: '1',
        }
        const username = $("#user-name").text();
        fetch(`/verifyresult/${username}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                request_type: 'json',
            })
        }).then(response => response.json())
        .then(data => {
            console.log(data);
            $('#time').text(data.time);
            $('#user-id').text(data.user_ID);
        }).catch(error => {
            console.log(error);
        });
    };

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


