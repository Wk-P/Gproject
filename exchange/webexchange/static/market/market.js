let marketdata = {}

window.onload = () => {
    marketdata = fetchMarketInformation();
}

window.addEventListener('scroll', () => {
    
})

function toString(json_data) {
    return JSON.stringify(json_data);
}

function fetchMarketInformation() {
    const csrftoken = getCookie('csrftoken')
    fetch("", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        }
    }).then(response => response.json())
    .then(data => {
        marketdata = data['data'];
        console.log(marketdata);
        for (item in marketdata) {
            li = document.createElement('li')
            li.textContent = toString(marketdata[item]['rank']) + " | " + toString(datai[item]['baseSymbol']) + " | " + toString(datai[item]['priceUsd']);
            $("#coin-item").append(li);
        }
    })
}