    window.onload = () => {
        const csrftoken = getCookie('csrftoken');
        const username = $("#user-name").text();
        fetch(`/verifyresult/${username}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                request_type: 'json',
            })
        }).then(response => response.json())
        .then(data => {
            // console.log(data);

            $('#time').text("2020-01-01");
            $('#user-id').text(data.user_ID);
            $('#merkle_root_hash').text(data.merkle_root_hash);
            $('#merkle_root_hash').text(data.merkle_root_hash);
            $('#zk_proof').text(data.zk_proof);
            $('#zk_verification_result').text(data.zk_verification_result);
            $('#assets').text(data.assets);
            $('#wallet_ID').text(data.wallet_ID);
            $('#asset_type').text(data.asset_type);
            $('#asset_amount').text(data.asset_amount);
            
        }).catch(error => {
            console.log(error);
        });
    };

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }