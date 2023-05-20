window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    // anv language change
    $('#language').on('change', (event) => {
        if (event.target.value === 'Chinese') {
            $('#coin').text(page_display_data.zh.nav.coin);
            $('#trade').text(page_display_data.zh.nav.exchanges);
            $('#swap').text(page_display_data.zh.nav.swap);
            $('#index').text(page_display_data.zh.nav.home);
            $("wallet-title").text()
        }
        else if (event.target.value === 'Korean') {
            $('#coin').text(page_display_data.kr.nav.coin);
            $('#trade').text(page_display_data.kr.nav.exchanges);
            $('#swap').text(page_display_data.kr.nav.swap);
            $('#index').text(page_display_data.kr.nav.home);
        }
        else {
            $('#coin').text(page_display_data.en.nav.coin);
            $('#trade').text(page_display_data.en.nav.exchanges);
            $('#swap').text(page_display_data.en.nav.swap);
            $('#index').text(page_display_data.en.nav.home);
        }
    });

    // get balances
    const username = $("#username").text().replace(' ', '')
    const data = {
        username: username,
        symbols: {
            btc: "BTC",
            eth: "ETH",
        }
    }
    // get user-data
    fetch(`/usercenter/${username}/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data) 
    }).then(response => response.json())
    .then((data) => {
        if (data.alert == null) {
            console.log("No Data");
        } else {
            let tbody = $("tbody");
            const history = data.trade_history
            for (let i = 0;i < history.length;i++) {
                let tr = document.createElement('tr');
                let action_td = document.createElement('td');
                let timestamp_td = document.createElement('td');
                let symbol_td = document.createElement('td');
                let amount_td = document.createElement('td');
                let chain_td = document.createElement('td');
                
                // add content to td
                
                action_td.innerHTML = history[i].action;
                timestamp_td.innerHTML = history[i].time_stamp;
                symbol_td.innerHTML = history[i].asset_type;
                amount_td.innerHTML = history[i].asset_amount;
                chain_td.innerHTML = history[i].chain;

                // add td into tr
                tr.appendChild(action_td);
                tr.appendChild(timestamp_td);
                tr.appendChild(symbol_td);
                tr.appendChild(amount_td);
                
                // add tr into tbody
                tbody.append(tr);
            }
        }
    }).catch(error => console.log(error))
}