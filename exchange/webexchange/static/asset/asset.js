function generate_table_contents(table_id, tr_size, td_id_arr, td_contents) {
    let table = document.getElementById(table_id)
    for (i in tr_size) {
        let tr = document.createElement('tr');
        for (td_id in td_id_arr) {
            td = document.createElement('td');
            td.id = td_id_arr[td_id];
            td.innerHTML = td_contents[td_id];
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
}

window.onload = () => {
    let btn_count = 1;

    const username = $("#user-name").html();
    const csrftoken = getCookie('csrftoken');
    const td_id_array = [
        `wallet_ID-${username}`,
        `chain-${username}`, 
        `coin_type-${username}`, 
        `amount-${username}`, 
        `veriy_btn-${username}`, 
        `status-${username}`
    ]
    let data = {
        username: username,
    }
    let params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }
    // For different post request
    data.click = 'no';
    params.body = JSON.stringify(data);

    table_id = "asset_list"

    fetch(`/asset/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log(data.asset_data);
            if (data.alert == 'success') {
                // asset data is completed

            } else if (data.alert == 'incomplete') {
                // asset data is None
                let table = document.getElementById(table_id);
                for (wallet_id of data.wallets_id) {
                    let tr = document.createElement('tr');
                    for (index in td_id_array) {
                        let td = document.createElement('td');
                        td.id = td_id_array[index]
                        if (td.id == `wallet_ID-${username}`) td.innerHTML = wallet_id;
                        if (td.id == `veriy_btn-${username}`) {
                            let btn = document.createElement('button');
                            btn.id = td.id + btn_count.toString();
                            btn.class = "verify_btn";
                            btn_count = btn_count + 1;
                            btn.innerHTML = 'Verify';
                            td.appendChild(btn);
                        }
                        else td.innerHTML = 'none';
                        tr.appendChild(td);
                    }
                    table.appendChild(tr);
                }
            }
            else {
                alert(data.alert);
            }
            td = document.createElement('td')
        })
        .catch(error => {console.log(error)});
}