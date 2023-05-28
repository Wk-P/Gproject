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
                const id_list = ['#c1', '#c2', "#c3", "#c4", "#c5", '#c6', "#c7", "#c8"]
                console.log(data.assets_data.length)
                for (let i = 0; i < id_list.length;i++) {
                    let symbol = "---"
                    let amount = 0
                    let ratio = 0
                    
                    if (i < data.assets_data.length) {
                        // receive data
                        symbol = data.assets_data[i].asset_type
                        amount = data.assets_data[i].asset_amount
                        ratio = parseFloat(Math.random() * (1.04 - 1.03) + 1.03);
                    }

                    // fill data

                    $(`${id_list[i]} coin-name name`).text(symbol)
                    $(`${id_list[i]} customer-balances`).text(amount);
                    $(`${id_list[i]} exchange-balances`).text((amount * ratio).toFixed(16));
                    $(`${id_list[i]} ratio`).text(`${(ratio * 100).toFixed(2)}%`);
                }
            }
        }).catch(error => console.log(error))
}