window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    const username = $("#user-name").html();
    let data = {
        username: username,
    }
    let params = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }
    
    data.register = 'no'
    params.body = JSON.stringify(data);
    let wallet_list = document.getElementById('wallet-table');
    fetch(`/wallet/${username}/`, params)
    .then(response => response.json())
    .then(data => {
        if (data.wallets_data == undefined) {
            // no wallets
            let tr = document.createElement('tr');
            let td = document.createElement('td');
            tr.id = 'no-register-tr';
            td.id = 'no-register-td';
            td.innerHTML = "No Registered Wallet";
            tr.appendChild(td);
            wallet_list.appendChild(tr);
        } else {
            // show wallets 
            for (item_data of data.wallets_data) {
                tr = document.createElement('tr');
                td = document.createElement('td');
                td.innerHTML = item_data.wallet_ID;
                tr.appendChild(td);
                wallet_list.appendChild(tr);
            }
        }
    })

    $("#add-button").click(() => {
        // register wallet
        data.register = 'yes';
        data.wallet_ID = $("#wallet-id").val()
        params.body = JSON.stringify(data);
        
        fetch(`/wallet/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            // add wallet data success
            if (data.register == 'success') {
                alert(`Register wallet ${data.wallet_id} success!`);
                tr = document.createElement('tr');
                td = document.createElement('td');
                td.innerHTML = data.wallet_id;
                tr.appendChild(td);
                wallet_list.appendChild(tr);
                $("#wallet-id").val("");
            }
            else {
                alert("Register Failed!");
            }
        })
        .catch(error => console.log(error));
    })
}