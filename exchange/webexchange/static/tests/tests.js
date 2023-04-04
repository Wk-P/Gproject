window.onload = () => {
    $("#test").onclick = () => {
        const csrf_token = getCookie("csrftoken");
        fetch("api.coincap.io/v2/markets", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                request_type: "json",
            })
        }).then(response => {
            response.json()   
        }).then(data => {
            $("#1").val(data)
        })
    }
}