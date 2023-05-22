window.onload = () => {

    const username = $("#username").text().replace(' ', '');
    const csrftoken = getCookie('csrftoken');
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
    // For default post request
    params.body = JSON.stringify(req_data);

    let tbody = $("#asset-tbody");
    fetch(`/asset/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            if (data.alert == 'success') {
                const asset_array = data.asset_data
                // asset data is completed
                if (asset_array.length > 0) {
                    for (let i = 0; i < asset_array.length; i++) {
                        let tr = document.createElement('tr');
                        let symbol_td = document.createElement('td');
                        let chain_td = document.createElement('td');
                        let amount_td = document.createElement('td');

                        symbol_td.innerHTML = asset_array[i].asset_type
                        chain_td.innerHTML = asset_array[i].chain
                        amount_td.innerHTML = asset_array[i].asset_amount

                        tr.appendChild(symbol_td)
                        tr.appendChild(chain_td)
                        tr.appendChild(amount_td)

                        tbody.append(tr)
                    }
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
        .catch(error => { console.log(error) });

    // display listener
    let display = false;



    // verify button click 
    $("#verify").click(() => {
        fetch(`/verify_callback/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                if (data.alert == 'success') {
                    console.log(data);
                    window.location.href = `/verify/${username}/`;
                } else {
                    // test
                    console.log(display)
                    if (display == false) {
                        console.log(data);
                        response = data['verify-result']
                        // result div
                        let result_div = document.createElement('div');
                        result_div.classList.add('result-div');
                        result_div.setAttribute('id', 'result')

                        // confirm button
                        let confirm_button = document.createElement('button');
                        confirm_button.setAttribute('id', 'confirm-btn');
                        confirm_button.innerHTML = "Confirm"


                        let li_list = {
                            'time': (() => {
                                let date = new Date();
                                let year = date.getFullYear()
                                let month = (date.getMonth() + 1) < 10 ? '0' + (date.getMonth() + 1) : (date.getMonth() + 1);
                                let day = date.getDate() < 10 ? '0' + (date.getDate()) : (date.getDate());
                                let hours = date.getHours() < 10 ? '0' + (date.getHours()) : (date.getHours());
                                let minutes = date.getMinutes() < 10 ? '0' + (date.getMinutes()) : (date.getMinutes());
                                let seconds = date.getSeconds() < 10 ? '0' + (date.getSeconds()) : (date.getSeconds());
                                return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
                            })(),
                            'merkle_root_hash': response.merkle_root_hash,
                            'zk_proof': response.zk_proof,
                            'zk_verification_result': response.zk_verification_result,
                            'wallet_ID': response.wallet_ID,
                            'assets': (() => {
                                let assets_str = new String();
                                for (let a of response.assets) {
                                   assets_str += `<br>Amount:${String(a.asset_amount)}`;
                                   assets_str += `<br>Symbol:${a.asset_type}`;
                                   assets_str += `<br>Chain:${a.chain}`;
                                }
                                return assets_str;
                            })(),
                        };

                        for (const li in li_list) {
                            let div = document.createElement('div');
                            div.innerHTML = `${li}<br>${li_list[li]}`;
                            div.setAttribute('id', li);
                            result_div.appendChild(div);
                        }

                        result_div.appendChild(confirm_button);
                        let parent = $(".result-parent");
                        parent.append(result_div);

                        // prevent append more div DOM node
                        display = true;

                        setTimeout(() => {
                            result_div.classList.add('show');
                        }, 100);
                    }
                }
            })
            .catch(error => console.log(error))
    })
    $(document).on('click', '#confirm-btn', () => {
        console.log(display)
        if (display == true) {
            let result_div = document.getElementById('result');

            // hidden DOM Element
            result_div.classList.add('hidden');
            display = false;

            // Listen for transitionend event
            result_div.addEventListener('transitionend', () => {
                // Remove result_div element
                result_div.remove();
            });
        }
    });
}