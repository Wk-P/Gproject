window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    const username = $("#user-name").text()
    $("#testbtn").click(() => {
        fetch(`/wallet/${username}`, {
            method: 'POST',
            headers: {
                'Context-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }).then(response => response.json())
        .then(data => {
                console.log(data.assets[0].wallet_ID);
                $("#test").text(data.assets[0].wallet_ID);
        });
    });
}