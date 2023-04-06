fetch('https://coincap.io/exchanges')
  .then(response => response.json())
  .then(data => {
    // 在这里处理返回的数据
    console.log(data);
  })
  .catch(error => {
    // 在这里处理请求失败的情况
    console.error(error);
  });



  fetch("", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
    }
}).then(response => response.json())
.then(data => {
    marketdata = data['data'];
    console.log(marketdata);
    for (item in marketdata) {
        li = document.createElement('li')
        li.textContent = toString(marketdata[item]['baseSymbol']) + " | " + toString(marketdata[item]['priceUsd']);
        $("#coin-item").append(li);
    }
})