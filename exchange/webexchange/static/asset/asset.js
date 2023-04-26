window.onload = () => {
    const username = $("#user-name").html();
    const csrftoken = getCookie('csrftoken');
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

    fetch(`/asset/${username}/`, params)
        .then(response => response.json())
        .then(data => {
            // tr = document.createElement('tr');
            console.log(data);
            td_array = [
                `wallet_ID-${username}`,
                `chain-${username}`, 
                `coin_type-${username}`, 
                `amount-${username}`, 
                `veriy_btn-${username}`, 
                `status-${username}`
            ]
            console.log(td_array);
            // td = document.createElement('td')
        })
        .catch(error => {console.log(error)})

}