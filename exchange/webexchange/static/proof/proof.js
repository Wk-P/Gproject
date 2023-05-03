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
        body: JSON.stringify(data) 
    }).then(response => response.json())
    .then((data) => {
        if (data.alert == "NO DATA") {
            console.log(data.alert);
        } else {
            $("#customer-balances").text(data.alert);
            $("#exchange-balances").text(data.balances * parseFloat(Math.random()*(1.34-1.03) + 1.03));
        }
    }).catch(error => console.log(error))
}