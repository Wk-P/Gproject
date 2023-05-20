window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    const username = $("#username").text().replace(' ','');
    let req_data = {
        username: username,
    }
    let params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }
    params.body = JSON.stringify(req_data);
    fetch(`/wallet/${username}/`, params)
    .then(response => response.json())
    .then(data => {
        console.log(data.asset_data);
        const asset_data = data.asset_data;
        
        let tbody = $("tbody")

        for (let ad of asset_data) {
            let wallet_td = document.createElement('td');
            let symbol_td = document.createElement('td');
            let amout_td = document.createElement('td');
            let chain_td = document.createElement('td');

            wallet_td.innerHTML = ad.wallet_ID;
            symbol_td.innerHTML = ad.symbol;
            amout_td.innerHTML = ad.amount;
            chain_td.innerHTML = ad.chain;
            
            let tr = document.createElement('tr');
            
            tr.appendChild(wallet_td);
            tr.appendChild(symbol_td);
            tr.appendChild(amout_td);
            tr.appendChild(chain_td);

            tbody.append(tr);
        }
    })
    .catch(error => console.log(error));

    $("#commit").click(() => {
        req_data.wallet_ID = $("#wallet-input").val().replace(' ','');
        params.body = JSON.stringify(req_data);
        fetch(`/walletadd/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            if (data == 'success') {
                alert(`Add New Wallet Successfully!\n${wallet_ID}`);
            }
            else {
                alert(data.alert);
            }
            $("#wallet-input").val("");
        })
        .catch(error => console.log(error))
    })
}