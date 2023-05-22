const max_size = 60;

function drawCandlestick(svg, trade_data, margin) {
    const highPrices = trade_data.map(v => v[2])
    const lowPrices = trade_data.map(v => v[3])
    const width = $("#chart").width() * 0.9;
    const height = $("#chart").height() * 0.9;

    svg.attr('width', width).attr('height', height);

    const dates = d3.map(trade_data, v => v[0])

    // delete old axis, rects, lines 
    svg.selectAll('.candles').remove()
    svg.selectAll('.gx').remove()
    svg.selectAll('.gy').remove()

    // update xScale and yScale
    const xScale = d3.scaleTime()
        .domain(d3.extent(dates))
        .range([margin.left, width - margin.right - margin.left])

    const yScale = d3.scaleLinear()
        .domain([Math.floor(d3.min(lowPrices)), Math.ceil(d3.max(highPrices))])
        .nice()
        .range([height - margin.bottom - 10, margin.top + 10])

    // generate axis
    const xAxis = d3.axisBottom(xScale)
        .tickValues(dates.filter((d, i) => i % 5 === 0))
        .tickFormat(d3.timeFormat('%M:%S'))

    const yAxis = d3.axisLeft(yScale)
        .tickValues(yScale.ticks().filter((d, i) => i % 2 === 0));

    // draw axis 
    svg.append('g')
        .classed('gx', true)
        .attr("transform", `translate(${margin.left}, ${height - margin.bottom})`)
        .call(xAxis)

    svg.append('g')
        .classed('gy', true)
        .attr("transform", `translate(${margin.left}, ${margin.top})`)
        .call(yAxis)

    // candles border color
    const handleStrokeColor = (v, i) => {
        if (v[1] > v[4]) {
            return 'green'
        }
        return 'red'
    }

    // calculate candles width
    const candlestickWidth = getCandlestickWidth(width, margin)

    // Create the main <g> element for the candlestick chart
    candles = svg.append('g')
        .classed('candles', true)
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const candlesticks = candles.selectAll('.candlestick')
        .data(trade_data)
        .enter()
        .append('g')
        .classed('candlestick', true)
        .attr('transform', (d) => `translate(${xScale(parseInt(d[0]))}, 0)`);

    candlesticks.append('rect')
        .classed('candlestick-rect', true)
        .attr('rx', 1)
        .attr('x', (d) => - candlestickWidth / 2)
        .attr('y', (d) => yScale(d3.max([d[1], d[4]])) - margin.top)
        .attr("width", candlestickWidth)
        .attr('height', (d) => Math.abs(yScale(d[1]) - yScale(d[4])) + 0.01)
        .attr('stroke', handleStrokeColor)
        .attr('fill', (d) => (d[1] > d[4]) ? 'green' : 'red');

    candlesticks.append('line')
        .classed('candlestick-line', true)
        .attr('x1', 0)
        .attr('y1', (d) => yScale(d[2]) - margin.top)
        .attr('x2', 0)
        .attr('y2', (d) => yScale(d[3]) - margin.top)
        .attr('stroke', handleStrokeColor)
        .attr('stroke-width', 1);
}

// 计算蜡烛图实线宽度
function getCandlestickWidth(width, margin) {
    return (width - margin.left - margin.right) / max_size * 0.8
}

function timetrans(time) {
    const date = new Date(time);
    const year = date.getFullYear().toString();
    const month = date.getMonth() < 9 ? '0' + (date.getMonth() + 1).toString() : (date.getMonth() + 1).toString();
    const day = date.getDate() < 10 ? '0' + (date.getDate() + 1).toString() : (date.getDate() + 1).toString();
    const hours = date.getHours() < 10 ? '0' + (date.getHours() + 1).toString() : (date.getHours() + 1).toString();
    const minutes = date.getMinutes() < 10 ? '0' + (date.getMinutes() + 1).toString() : (date.getMinutes() + 1).toString();
    const seconds = date.getSeconds() < 10 ? '0' + (date.getSeconds() + 1).toString() : (date.getSeconds() + 1).toString();

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

function formatText(v) {
    return `${timetrans(v[0])}
    开盘: ${v[1]} |
    收盘: ${v[4]} |
    最高: ${v[2]} |
    最低: ${v[3]}`
}

window.onload = () => {
    const username = $("#username").text().replace(' ', '');
    const csrftoken = getCookie('csrftoken');
    let req_data = {
        username: username,
        reqtype: ""
    }

    let params = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }

    // test flag
    let i = 0;

    let buy_orders = new Array()
    let sell_orders = new Array()
    let finish_orders = new Array()

    // get orders
    setInterval(() => {
        params.body = JSON.stringify(req_data);
        fetch(`/trade_orders/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                let sell_tbody = $("#sell tbody");
                let buy_tbody = $("#buy tbody");
                let finish_tbody = $("#trade-details tbody");

                // add buy orders 
                buy_orders = data.buy_orders;
                console.log(buy_orders)
                buy_tbody.empty()
                if (buy_orders !== undefined) {
                    for (let i in buy_orders) {
                        let tr = document.createElement('tr');
                        let name_td = document.createElement('td');
                        let price_td = document.createElement('td');
                        let quantity_td = document.createElement('td');

                        // add data
                        name_td.innerHTML = buy_orders[i].stock_name;
                        price_td.innerHTML = buy_orders[i].price;
                        quantity_td.innerHTML = buy_orders[i].quantity;

                        tr.appendChild(name_td);
                        tr.appendChild(price_td);
                        tr.appendChild(quantity_td);
                        tr.setAttribute('class', 'ordertr');
                        buy_tbody.append(tr);
                    }
                }

                // add sell orders
                sell_orders = data.sell_orders;
                console.log(sell_orders)
                sell_tbody.empty();
                if (sell_orders !== undefined) {
                    for (let i in sell_orders) {
                        let tr = document.createElement('tr');
                        let name_td = document.createElement('td');
                        let price_td = document.createElement('td');
                        let quantity_td = document.createElement('td');

                        // add data
                        name_td.innerHTML = sell_orders[i].stock_name;
                        price_td.innerHTML = sell_orders[i].price;
                        quantity_td.innerHTML = sell_orders[i].quantity;

                        tr.appendChild(name_td);
                        tr.appendChild(price_td);
                        tr.appendChild(quantity_td);
                        tr.setAttribute('class', 'ordertr');

                        sell_tbody.append(tr);
                    }
                }

                // add finish orders
                finish_orders = data.ordered
                console.log(finish_orders)
                finish_tbody.empty();
                if (finish_orders !== undefined) {
                    for (let i in finish_orders) {
                        let tr = document.createElement('tr');
                        let name_td = document.createElement('td');
                        let price_td = document.createElement('td');
                        let quantity_td = document.createElement('td');

                        // add data
                        name_td.innerHTML = finish_orders[i].stock_name;
                        price_td.innerHTML = finish_orders[i].price;
                        quantity_td.innerHTML = finish_orders[i].quantity;
                        tr.appendChild(name_td);
                        tr.appendChild(price_td);
                        tr.appendChild(quantity_td);
                        tr.setAttribute('class', 'ordertr');

                        finish_tbody.append(tr);
                    }
                }
            })
            .catch(error => console.log(error));
    }, 500)

    $("#buy-btn").click(() => {
        let order = {
            type: 'buy',
            timestamp: new Date().getTime(),
            stockname: $("#stock-name input").val(),
            quantity: parseInt($("#quantity input").val()),
            price: parseFloat($("#price input").val()),
        }
        req_data.order = order
        req_data.reqtype = 'trade';

        console.log(order.stockname, order.price, order.quantity)

        if (order.stockname == "" || order.quantity == NaN || order.price == NaN) {
            alert("Enter stock name or amount!"); return
        }

        if (order.quantity <= 0 || order.price <= 0) {
            alert("Enter correct price or quantity!"); return
        }

        params.body = JSON.stringify(req_data);
        fetch(`/trade_orders/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                alert(data.alert);
                $("#stock-name input").val("");
                $("#quantity input").val("");
                $("#price input").val("");
            })
            .catch(error => console.log(error))

        // reset request json data
        req_data.reqtype = ""
    });

    $("#sell-btn").click(() => {
        var order = {
            type: 'sell',
            timestamp: new Date().getTime(),
            stockname: $("#stock-name input").val(),
            quantity: parseInt($("#quantity input").val()),
            price: parseFloat($("#price input").val()),
        }
        req_data.order = order
        req_data.reqtype = 'trade';


        if (order.stockname == "" || order.quantity == NaN || order.price == NaN) {
            alert("Enter stock name or amount!"); return
        }

        if (order.quantity <= 0 || order.price <= 0) {
            alert("Enter correct price or quantity!"); return
        }

        params.body = JSON.stringify(req_data)
        fetch(`/trade_orders/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                alert(data.alert);
                $("#stock-name input").val("");
                $("#quantity input").val("");
                $("#price input").val("");
            })
            .catch(error => console.log(error))

        // reset request json data
        req_data.reqtype = ""
    });


    var trade_data = new Array();
    const width = $("#chart").width() * 0.9;
    const height = $("#chart").height() * 0.9;
    const margin = { top: 10, right: 30, bottom: 30, left: 50 };

    let svg = d3.select('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])

    // Initialize x , y Axis
    // let xScale = drawAxisX(svg, width, height, margin);
    // let yScale = drawAxisY(svg, height, margin);

    var text = svg.append('text');

    text.selectAll('*').remove();
    text.attr('x', width - margin.right)
        .attr('y', margin.top / 2)
        .attr('font-size', '0.85em')
        .attr('fill', '#666')
        .attr('text-anchor', 'end')
        .attr('dominant-baseline', 'hanging')


    // 使用setTimeout函数延迟数据处理
    params.body = JSON.stringify(req_data);
    try {
        setInterval(() => {
            fetch(`/trade_websocket/`, params)
                .then(response => response.json())
                .then(data => {
                    // push data to array with out shift
                    if (trade_data.length >= max_size) {
                        trade_data.shift()
                    }
                    trade_data.push([data.price_data.k.T,
                    parseFloat(data.price_data.k.o),
                    parseFloat(data.price_data.k.h),
                    parseFloat(data.price_data.k.l),
                    parseFloat(data.price_data.k.c)])
                    text.text(formatText(trade_data[trade_data.length - 1]))

                    drawCandlestick(svg, trade_data, margin)
                })
        }, 1000)
    }
    catch (error) {
        console.error(error)
    }
}
