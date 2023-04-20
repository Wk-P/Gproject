window.onload = () => {
    const td_id = ['rank', 'name', 'price', 'market-cap', 'vmap', 'supply', 'volume', 'change'];
    $("#zhongwen").cilck(() => {
        $("#shizhi").val("市值");
    })
    fetchMarketInformation().then(data => {
        const intervalId = setInterval(() => {
            if (data['assets_data'].length) {
                clearInterval(intervalId);
                for (let i = 0;i < 20;i++) {
                    let tr = document.createElement('tr');
                    const item = (data['assets_data'])[i];
                    console.log(item);
                    tr.id = item['id'];
                    for (const id of td_id) {
                        let td = document.createElement('td');
                        td.id = id;
                        if (id === 'rank') td.innerHTML = item['rank'];
                        else if (id === 'name') td.innerHTML = item['name'];
                        else if (id === 'price') td.innerHTML = item['priceUsd'];
                        else if (id === 'vmap') td.innerHTML = item['vwap24Hr'];
                        else if (id === 'supply') td.innerHTML = item['supply'];
                        else if (id === 'market-cap') td.innerHTML = item['marketCapUsd'];
                        else if (id === 'volume') td.innerHTML = item['volumeUsd24Hr'];
                        else if (id === 'change') td.innerHTML = item['changePercent24Hr'];
                        tr.appendChild(td);
                    }
                    $('#coin-item').append(tr);
                }
            }
        }, 10);

        setInterval(() => {
            fetchMarketInformation().then(data => {
                const prices_data = data['prices-data'];
                for (const coin in prices_data) {
                    const price = $('#' + coin + ' > td[id="price"]');
                    price.html(prices_data[coin]);
                    fadeOut($('#' + coin));
                }
            }).catch(error => console.log(error));
        }, 1000);
    });
};

function toString(json_data) {
    return JSON.stringify(json_data);
}

function fetchMarketInformation() {
    const csrftoken = getCookie('csrftoken');
    return fetch(`/coins/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => console.log(error));
}

function fadeOut(element) {
    // animation
    element.removeClass('fade-out');
    element.addClass('fade-in');
    setTimeout(() => {
        element.removeClass('fade-in');
        element.addClass('fade-out');
    }, 500);
}


