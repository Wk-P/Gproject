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
        `chain-${username}`, 
        `cointype-${username}`, 
        `amount-${username}`, 
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

    tbody = $("#asset-tbody");
    table = $("table");

    fetch(`/asset/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            // console.log(data.asset_data);
            if (data.alert == 'success') {
                // asset data is completed
                if (data.asset_data != null) {
                    tr = document.createElement('tr');
                } else {
                    let div = document.createElement('div')
                    div.innerHTML = "No Asset Data";
                    div.id = 'no-asset-data';
                    table.after(div);
                }
            }
            else {
                alert(data.alert);
            }
            td = document.createElement('td')
        })
        .catch(error => {console.log(error)});
}