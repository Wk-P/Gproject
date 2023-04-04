window.onload = () => {
    $("#test").click(() => {
        const csrftoken = getCookie("csrftoken");
        fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            $("#in").val(data);
        });
    })
}