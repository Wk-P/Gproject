window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    $("#submit").click((event) => {
        event.preventDefault();        // prevent to jump a new page
        const data = {
            click: 'submit',
            'username': $('#username').val(),
            'userpassword': $('#userpassword').val(),
        };

        fetch(`/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (data['alert'] != 'success') {
                    alert(data['alert']);
                    $('#username').val("");
                    $('#userpassword').val("");
                } else if (data['alert'] == null) {
                    // no operator
                } else {
                    window.location.href = `/main/${data['username']}/`;
                }
            })
            .catch(error => console.log(error));
    });
    // request to login backend code and response is OK to jump a new page
    $("#cancel").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'cancel',
        }
        jumpTo(`/login/`, '/', data, csrftoken, 'POST');
    });
    $("#register").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'register',
        }
        jumpTo(`/login/`, '/register/', data, csrftoken, 'POST');
    });
}