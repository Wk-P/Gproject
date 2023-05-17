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
    const username = $("#username").text().replace(' ', '')
    const data = {
        username: username,
        symbols: {
            btc: "BTC",
            eth: "ETH",
        }
    }

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
            $("#customer-balances").text(data.user_data);
        }
    }).catch(error => console.log(error))
}