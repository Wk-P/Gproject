window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    const page_body_display = {
        zh: {
            "wallet-title": "钱包地址",
        },
        en: {
            "wallet-title": "Wallet Address",
        },
        kr: {
            "wallet-title": "지갑 주소",
        }
    }
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

    const username = $("#username").text().replace(' ', '')
    let req_data = {
        username: username,
    }
    let params = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }
    $("#confirm").click(() => {
        const send_out_wallet_address = $("#send-out-wallet-address").val().replace(' ', '');
        const send_in_wallet_address = $("#send-in-wallet-address").val().replace(' ', '');
        const amount = parseFloat($("#coin-amount").val());
        const symbol = $("coin-type select option:selected").text().replace(' ', '');
        const chain = $("chain-type select option:selected").text().replace(' ', '');

        if (send_out_wallet_address == "" || send_in_wallet_address == "" || amount <= 0 || amount === NaN) {
            alert("Wrong input!");
            return;
        }
        // wallet address value
        req_data.send_out_wallet_address = send_out_wallet_address;
        req_data.send_in_wallet_address = send_in_wallet_address;
        // symbol type
        req_data.symbol = symbol;
        req_data.chain = chain;
        req_data.amount = amount;

        params.body = JSON.stringify(req_data);
        fetch(`/transaction/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                if (data.alert == 'success') {
                    alert(`Success:\nFrom ${send_out_wallet_address} to ${send_in_wallet_address}, Amount: ${amount}, Symbol: ${symbol}, Chain: ${chain}\ncurrency transfer completed!\n`);
                } else {
                    console.log(data)
                    alert(data.alert);
                }
            })
            .catch(error => console.log(error))
    })
    $("#cancel").click(() => {
        $("#send-out-wallet-address").val("")
        $("#send-in-wallet-address").val("")
        $("#coin-amount").val("")
    })
}