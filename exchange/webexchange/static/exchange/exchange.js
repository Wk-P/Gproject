/*

fetch('https://coincap.io/exchanges')
  .then(response => response.json())
  .then(data => {
    // 在这里处理返回的数据
    console.log(data);
  })
  .catch(error => {
    // 在这里处理请求失败的情况
    console.error(error);
  });



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
        li.textContent = toString(marketdata[item]['baseSymbol']) + " | " + toString(marketdata[item]['priceUsd']);
        $("#coin-item").append(li);
    }
})
*/

window.onload = () => {
    const td_id = ['Rank', 'Name', 'Trading Pairs', 'Volume(24Hr)', 'Total', 'Status'];

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
                        if (id === 'Rank') td.innerHTML = item['Rank'];
                        else if (id === 'Name') td.innerHTML = item['Name'];
                        else if (id === 'Trading Pairs') td.innerHTML = item['Trading Pairs'];
                        else if (id === 'Volume(24Hr)') td.innerHTML = item['Volume(24Hr)'];
                        else if (id === 'Total') td.innerHTML = item['Total'];
                        else if (id === 'Status') td.innerHTML = item['Status'];
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


