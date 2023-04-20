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
                console.log(data.assets);
                assets = data.assets
                for (var i in assets) {
                    for (var j in assets[i]) {
                        if (j != 'wallet_ID') {
                            $("#test").text($("#test").text() + " | " + assets[i][j]);
                        } else {
                            $("#test").text(assets[i][j]);
                        }
                    }
                }
            });
    });
}