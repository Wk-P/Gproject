let marketdata = {}

window.onload = () => {
    setInterval(() => {
        fetchMarketInformation();
        console.log(marketdata);
    }, 1000);
}

function toString(json_data) {
    return JSON.stringify(json_data);
}

function fetchMarketInformation() {
    const csrftoken = getCookie('csrftoken');
    fetch(`/market/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        }
    }).then(response => response.json())
    .then(data => {
        console.log(JSON.stringify(data['prices-data']));
        $("#coin-item").html(JSON.stringify(data['prices-data']));
    })
}