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


    const scales = [xScale, yScale];
    return scales;
}

function drawFocusLayout(svg, trade_data, width, height, xScale, yScale, margin, text, formatText) {
    // 计算蜡烛图实线宽度
    const candlestickWidth = getCandlestickWidth(width, margin)

    // 鼠标移入事件
    const handleMouseOver = function (e) {
        d3.select('#focusLineX').attr('display', '')
        d3.select('#focusLineY').attr('display', '')
    }

    // 鼠标在图表中移动事件
    const handleMouseMove = function (e) {
        const [mx, my] = d3.pointer(e)
        const i = d3.bisectCenter(trade_data.map((v, i) => i), xScale.invert(mx - margin.left));
        const px = xScale(i) + margin.left + candlestickWidth / 2
        const py = height - yScale(trade_data[i][2]) - margin.bottom
        d3.select('#focusLineX').attr('x1', px).attr('x2', px)
        d3.select('#focusLineY').attr('y1', py).attr('y2', py)
        text.text(formatText(trade_data[i]))
    }

    // 涨跌幅: ${v[6]}% |
    // 鼠标移出事件
    const handleMouseOut = function (e) {
        d3.select('#focusLineX').remove()
        d3.select('#focusLineY').remove()
        text.text(formatText(trade_data[trade_data.length - 1]))
    }
    // 绘制标识线
    svg.append('line')
        .attr('id', 'focusLineX')
        .attr('x1', margin.left)
        .attr('y1', margin.top)
        .attr('x2', margin.left)
        .attr('y2', height - margin.bottom)
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 1)
        .attr('opacity', 0.5)
        .attr('display', 'none')

    svg.append('line')
        .attr('id', 'focusLineY')
        .attr('x1', margin.left)
        .attr('y1', margin.top)
        .attr('x2', width - margin.right)
        .attr('y2', margin.top)
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 1)
        .attr('opacity', 0.5)
        .attr('display', 'none')

    // 绘制鼠标事件触发区域
    svg.append('rect')
        .attr('x', margin.left)
        .attr('y', margin.top)
        .attr('width', width - margin.left - margin.right)
        .attr('height', height - margin.top - margin.bottom)
        .attr('opacity', 0)
        .on('mouseover', handleMouseOver)
        .on('mousemove', handleMouseMove)
        .on('mouseout', handleMouseOut)
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
    const username = $("#username").text();
    const csrftoken = getCookie('csrftoken');
    let data = {
        username: username,
        reqtype: ['match'],
    }

    let params = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }

    $("#buy-btn").click(() => {
        var order = {
            type: 'buy',
            timestamp: new Date().getTime(),
            stockname: $("#stock-name input").val(),
            quantity: parseInt($("#quantity input").val()),
            price: parseFloat($("#price input").val()),
        }
        data.order = order
        data.reqtype.push('trade');

        if (order.stockname == undefined || order.quantity == undefined || order.price == undefined) {
            alert("Enter stock name or amount!");
        }

        if (order.quantity <= 0 || order.price <= 0) {
            alert("Enter correct price or quantity!")
        }

        params.body = JSON.stringify(data);
        fetch(`/trade/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                alert(data.alert);
            })
            .catch(error => console.log(error))
    });

    $("#sell-btn").click(() => {
        var order = {
            type: 'sell',
            timestamp: new Date().getTime(),
            stockname: $("#stock-name input").val(),
            quantity: parseInt($("#quantity input").val()),
            price: parseFloat($("#price input").val()),
        }
        data.order = order
        data.reqtype.push('trade');

        if (order.stockname == undefined || order.quantity == undefined || order.price == undefined) {
            alert("Enter stock name or amount!");
        }

        if (order.quantity <= 0 || order.price <= 0) {
            alert("Enter correct price or quantity!")
        }

        params.body = JSON.stringify(data)
        fetch(`/trade/${username}/`, params)
            .then(response => response.json())
            .then(data => {
                alert(data.alert);
            })
            .catch(error => console.log(error))
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
    params.body = JSON.stringify(data);
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

                    const scales = drawCandlestick(svg, trade_data, margin)
                    // drawFocusLayout(svg, trade_data, width, height, scales[0], scales[1], margin, text, formatText)
                })
        }, 1000)
    }
    catch (error) {
        console.error(error)
    }
}
