window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    let params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }
    $("#login").click((event) => {
        event.preventDefault();
        const username = $("#username").val().replace(' ','');
        const password = $("#userpassword").val().replace(' ','');

        if (username === "" || password === "") {
            alert("Empty input!");
            $("#username").val("");
            $("#userpassword").val("");
        }

        let req_data = {
            username: username,
            password: password,
        }

        params.body = JSON.stringify(req_data);
        fetch(`/walletlogin/`, params)
        .then(response => response.json())
        .then(data => {
            if (data.alert == 'success') {
                window.location.href = `/wallet/${username}/`;
            } else {
                alert(data.alert);
                $("#username").val("");
                $("#userpassword").val("");
            }
        })
    })
}