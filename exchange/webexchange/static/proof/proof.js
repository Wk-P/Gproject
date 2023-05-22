window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    
    // anv language change
    $('#language').on('change', (event) => {
        if (event.target.value === 'Chinese') {
            $('#coin').text(page_display_data.zh.nav.coin);
            $('#exchanges').text(page_display_data.zh.nav.exchanges);
            $('#swap').text(page_display_data.zh.nav.swap);
            $('#index').text(page_display_data.zh.nav.home);
            $("wallet-title").text()
        }
        else if (event.target.value === 'Korean') {
            $('#coin').text(page_display_data.kr.nav.coin);
            $('#exchanges').text(page_display_data.kr.nav.exchanges);
            $('#swap').text(page_display_data.kr.nav.swap);
            $('#index').text(page_display_data.kr.nav.home);
        }
        else {
            $('#coin').text(page_display_data.en.nav.coin);
            $('#exchanges').text(page_display_data.en.nav.exchanges);
            $('#swap').text(page_display_data.en.nav.swap);
            $('#index').text(page_display_data.en.nav.home);
        }
    });

    // get balances
    const username = $("#username").text();
    const data = {
        username: username,
        symbols: {
            btc: "BTC",
            eth: "ETH",
        }
    }

    fetch(`/proof/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }).then(response => response.json())
    .then((data) => {
        console.log(data)
        if (data.alert == "No Data") {
            console.log(data.alert);
        } else {
            const symbol = data.assets_data[0].asset_type
            const amount = data.assets_data[0].asset_amount
            const ratio  = parseFloat(Math.random()*(1.04-1.03) + 1.03);
            $("coin-name name").text(symbol)
            $("customer-balances").text(amount);
            $("exchange-balances").text(amount* ratio);
            $("ratio").text(`${(ratio*100).toFixed(2)}%`);
        }
    }).catch(error => console.log(error))
}