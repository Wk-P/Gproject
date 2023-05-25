function toString(json_data) {
    return JSON.stringify(json_data);
}
function fetchMarketInformation() {
    const csrftoken = getCookie('csrftoken');
    return fetch(`/coins_websocket/`, {
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



window.onload = () => {
    const td_id = ['rank', 'name', 'price', 'market-cap', 'vmap', 'supply', 'volume', 'change'];

    let updatepage = true;
    setInterval(() => {
        fetchMarketInformation()
            .then(data => {
                if (updatepage) {
                    if (data['assets-data'].length) {
                        for (let i = 0; i < 20; i++) {
                            let tr = document.createElement('tr');
                            const item = (data['assets-data'])[i];
                            tr.id = item['id'];
                            for (const id of td_id) {
                                let td = document.createElement('td');
                                td.id = id;
                                if (id === 'rank') td.innerHTML = item['rank'];
                                else if (id === 'name') td.innerHTML = item['name'];
                                else if (id === 'price') td.innerHTML = parseFloat(item['priceUsd']).toFixed(2);
                                else if (id === 'vmap') td.innerHTML = parseFloat(item['vwap24Hr']).toFixed(2);
                                else if (id === 'supply') td.innerHTML = parseFloat(item['supply']).toFixed(2);
                                else if (id === 'market-cap') td.innerHTML = parseFloat(item['marketCapUsd']).toFixed(2);
                                else if (id === 'volume') td.innerHTML = parseFloat(item['volumeUsd24Hr']).toFixed(2);
                                else if (id === 'change') td.innerHTML = parseFloat(item['changePercent24Hr']).toFixed(2);
                                tr.appendChild(td);
                            }
                            $('#coin-item').append(tr);
                        }
                    }
                    updatepage = false
                } else {
                    if (data['assets-data'].length) {
                        let tr_list = $("#coin-item tbody tr");
                        for (let i = 0; i < tr_list.length; i++) {
                            let tr = tr_list[i];
                            const item = (data['assets-data'])[i];
                            for (const j in td_id) {
                                let td = tr.eq(j)
                                td.id = id;
                                if (id === 'rank') td.innerHTML = item['rank'];
                                else if (id === 'name') td.innerHTML = item['name'];
                                else if (id === 'price') td.innerHTML = parseFloat(item['priceUsd']).toFixed(2);
                                else if (id === 'vmap') td.innerHTML = parseFloat(item['vwap24Hr']).toFixed(2);
                                else if (id === 'supply') td.innerHTML = parseFloat(item['supply']).toFixed(2);
                                else if (id === 'market-cap') td.innerHTML = parseFloat(item['marketCapUsd']).toFixed(2);
                                else if (id === 'volume') td.innerHTML = parseFloat(item['volumeUsd24Hr']).toFixed(2);
                                else if (id === 'change') td.innerHTML = parseFloat(item['changePercent24Hr']).toFixed(2);
                            }
                        }
                    }
                }

                const prices_data = data['prices-data'];
                for (const coin in prices_data) {
                    const price = $('#' + coin + ' > td[id="price"]');
                    price.html(prices_data[coin]);
                    fadeOut($('#' + coin));
                }
            })
            .catch(error => console.log(error));
    }, 1000);
}