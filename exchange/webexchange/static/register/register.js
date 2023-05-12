window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    $("#submit").click((event) => {
        event.preventDefault();        // prevent to jump a new page
        const data = {
            'click': 'submit',
            'username': $('#name_input').val(),
            'userpassword': $('#password').val(),
            'userpassworda': $('#passworda').val()
        };

        fetch(`/register/`, {
            method: "POST",
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
                    $('#name_input').val("");
                    $('#password').val("");
                    $('#passworda').val("");
                } else if (data['alert'] == null) {
                    // no operator
                } else {
                    // register success jump to main page
                    // console.log(data)
                    // console.log(data.username)
                    window.location.href = `/main/${data.username}/`;
                }
            })
            .catch(error => console.log(error));
    });
    $("#login").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'login',
        }
        jumpTo(`/register/`, '/login/', data, csrftoken, 'POST');
    });
    $("#cancel").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'cancel',
        }
        console.log(getCookie);
        jumpTo(`/register/`, '/', data, csrftoken, 'POST');
    });
}