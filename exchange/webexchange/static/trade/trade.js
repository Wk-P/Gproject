// function timetrans(date) {
//     var date = new Date(date);//如果date为13位不需要乘1000
//     var Y = date.getFullYear() + '-';
//     var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
//     var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
//     var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
//     var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
//     var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
//     return Y + M + D + h + m + s;
// }

// window.onload = () => {


//     // 定义画布宽度、高度和边距
//     const width = $("#chart").width() * 0.9;
//     const height = $("#chart").height() * 0.9;
//     const margin = { top: 10, right: 30, bottom: 30, left: 60 };


//     // 创建SVG元素
//     const svg = d3.select('#chart')
//         .append('svg')
//         .attr('width', width,)
//         .attr('height', height,);




//     // 获取当前交易对的价格
//     // const symbol = 'BTC_USDT';
//     // fetch(`https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`, { mode: 'cors' })
//     //     .then(response => response.json())
//     //     .then(data => console.log(`当前 ${symbol} 价格为 ${data.price}`))
//     //     .catch(error => console.error(error));



//     // 订阅 WebSocket 实时推送的 K 线数据
//     const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@kline_1s');




//     ws.onmessage = event => {
//         const data = JSON.parse(event.data);
//         console.log('hightest price: ', data.k.h);
//         console.log('lowest price: ', data.k.l);
//         console.log('open price: ', data.k.o);
//         console.log('close price: ', data.k.c);
//         console.log('time:', timetrans(data.k.T));
//         const trade_data = [
//             { time: timetrans(data.k.T), open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c },
//             { time: timetrans(data.k.T), open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c },
//             // { time: '2021-01-03', open: 10500, high: 11000, low: 10000, close: 10200 },


//         ];

//         // 定义K线图的比例尺和坐标轴
//         const xScale = d3.scaleBand().range([margin.left, width - margin.right]);
//         const yScale = d3.scaleLinear().range([height - margin.bottom, margin.top]);
//         const xAxis = d3.axisBottom(xScale);
//         const yAxis = d3.axisLeft(yScale);

//         // 更新K线图
//         const updateChart = (trade_data) => {
//             // 计算比例尺的域
//             const minTime = d3.min(trade_data, d => d.time);
//             const maxTime = d3.max(trade_data, d => d.time);
//             const minValue = d3.min(trade_data, d => d.low);
//             const maxValue = d3.max(trade_data, d => d.high);


//             // 更新比例尺的域
//             xScale.domain(trade_data.map(d => new Date(d.time)));
//             yScale.domain([minValue, maxValue]);

//             // 添加坐标轴
//             svg.select('.x-axis')
//                 .attr('transform', `translate(0, ${height - margin.bottom})`)
//                 .call(xAxis);



//             svg.select('.y-axis')
//                 .attr('transform', `translate(${margin.left}, 0)`)
//                 .call(yAxis);

//             // 更新K线图的数据
//             const candles = svg.selectAll('.candle').data(trade_data);

//             // 移除已经不存在的数据
//             candles.exit().remove();

//             // 添加新的K线图数据
//             const newCandles = candles.enter()
//                 .append('g')
//                 .attr('class', 'candle')
//                 .attr('transform', d => `translate(${xScale(new Date(d.time)) - xScale.bandwidth() / 20}, 0)`);


//             var color = 'green';
//             newCandles.append('line')
//                 .attr('class', 'high-low')
//                 .attr('x1', xScale.bandwidth() / 5)
//                 .attr('x2', xScale.bandwidth() / 5)
//                 .attr('y1', d => yScale(d.high))
//                 .attr('y2', d => yScale(d.low))
//                 .attr('stroke', d => d.open < d.close ? 'green' : 'red');

//             var color_two = 'red';

//             newCandles.append('rect')
//                 .attr('class', 'open-close')
//                 .attr('x', 0)
//                 .attr('y', d => yScale(Math.max(d.open, d.close)))
//                 .attr('width', xScale.bandwidth() / 5)   //柱宽
//                 .attr('fill', d => d.open < d.close ? 'green' : 'red')
//                 .attr('height', d => {
//                     if (d.open === d.close) {
//                         return 1;
//                     } else {
//                         return yScale(Math.min(d.open, d.close)) - yScale(Math.max(d.open, d.close));
//                     }
//                 });

//                 // 更新K线图的位置和大小
//                 candles.merge(newCandles)
//                 .transition()
//                 .duration(1000)
//                 .attr('transform', d => `translate(${xScale(new Date(d.time)) - xScale.bandwidth() / 20}, 0)`);

//               candles.merge(newCandles)
//                 .select('.high-low')
//                 .transition()
//                 .duration(1000)
//                 .attr('y1', d => yScale(d.high))
//                 .attr('y2', d => yScale(d.low))
//                 .attr('stroke', d => d.open < d.close ? color : color_two);

//               candles.merge(newCandles)
//                 .select('.open-close')
//                 .transition()
//                 .duration(1000)
//                 .attr('y', d => yScale(Math.max(d.open, d.close)))
//                 .attr('height', d => d.open === d.close ? 1 : Math.abs(yScale(d.open) - yScale(d.close)))
//                 .attr('fill', d => d.open < d.close ? color : color_two);


//             }
//         updateChart(trade_data)
//         // console.log(updateChart);

//         // 选中DOM元素并添加事件监听
//         $('#time-buttons button').on('click', function () {
//             // 处理事件
//         });





//         // 连接服务器
//         // const socket = io.connect('http://localhost');

//         // 监听事件
//         // socket.on('update', function (data) {
//         // 更新数据
//         // });
//     }
// }    


const margin = { top: 10, right: 30, bottom: 30, left: 60 };

// 绘制标题
function drawTitle(value, svg, margin) {
    svg.append('text')
        .text(value)
        .attr('x', margin.left)
        .attr('y', margin.top / 2)
        .attr('text-anchor', 'start')
        .attr('dominant-baseline', 'hanging')
}




function timetrans(date) {
    var date = new Date(date);//如果date为13位不需要乘1000
    var Y = date.getFullYear() + '';
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '';
    var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + '';
    var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + '';
    var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + '';
    var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
    return Y + M + D + h + m + s;
}



// 绘制横坐标
function drawAxisX(svg, width, height, margin) {
    // const dates = d3.map(trade_data, v => v[0])

    var scale = d3.scaleLinear()
        // .domain([1, 10]) //x轴的取值范围
        .range([0, width - margin.left - margin.right])

    var axis = d3.axisBottom(scale)
        .ticks(10) //x轴上面取值范围分为几分
    // .tickFormat(v => {
    // return dates[v]
    // })

    var g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + (height - margin.bottom) + ')')
        .call(axis)




    return g
}

// 绘制竖标轴
function drawAxisY(svg, width, height, margin) {
    // 找到最高价和最低价，用来作为蜡烛图的参照坐标
    //  const highPrices = d3.map(trade_data, v => v[2])
    //  const lowPrices = d3.map(trade_data, v => v[3])


    //调整比例尺的定义域
    //const pricePending = Math.round(d3.max(highPrices) / 100)

    // 绘制竖坐标
    const scale = d3.scaleLinear()
        //  .domain([d3.min(lowPrices) - pricePending, d3.max(highPrices) + pricePending])
        .range([height - margin.top - margin.bottom, 0])


    //创建y轴刻度线生成器
    const axis = d3.axisLeft(scale).ticks(10)

    var g = svg.append('g')
    g.attr('transform', 'translate(' + (margin.left - 5) + ', ' + margin.top + ')')
        .call(axis)
        //.call(g => g.select('.domain').remove())
        .call(g => {
            g.selectAll('.tick line')
                .clone()
                .attr('stroke-opacity', 0.1)
                .attr('stroke-dasharray', 5)
                .attr('x2', width - margin.left - margin.right)
        })

    return axis
}



function drawCandlestick(svg, width, height, trade_data, gx, yScale, margin) {
    console.log(trade_data)
    const highPrices = d3.map(trade_data, v => v[2])
    const lowPrices = d3.map(trade_data, v => v[3])
    const pricePending = Math.round(d3.max(highPrices) / 100)

    var dates = d3.map(trade_data, v => v[0])


    // const parseTime = d3.timeParse('%s');
    // dates = dates.map(d => parseTime(d));

    console.log(dates, parseInt(dates[0]))

    let datesObjects = []
    for (let i = 0;i < 10;i++) {
        if (i < length) {
            datesObjects[i] = dates[i]
        }
        else {
            datesObjects[i] = dates[0] + i;
        }
    }
    
    const xScale = d3.scaleLinear()
        .domain([parseInt(datesObjects[0]), parseInt(datesObjects[datesObjects.length - 1])])
        .range([0, width - margin.left - margin.right])

    const axis = d3.axisBottom(xScale)
        .tickValues(datesObjects)
        .tickFormat(d3.format("d"))
    gx.call(axis);


    // 定义新的x轴比例尺

    // 更新x轴比例尺属性


    yScale.domain([d3.max(highPrices) + pricePending, d3.min(lowPrices) - pricePending])


    // 处理蜡烛图边框颜色
    const handleStrokeColor = (v, i) => {
        if (v[1] > v[2]) {
            return 'green'
        }

        return 'red'
    }

    // 计算蜡烛图实线宽度
    // const candlestickWidth = getCandlestickWidth(data.length)
    const candlestickWidth = 10
    const g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

    const candlestick = g.selectAll('g')
        .data(trade_data)
        .enter()
        .append('g')

    candlestick.append('line')
        .attr('x1', (v, i) => {
            return xScale(i) + candlestickWidth / 2
        })
        .attr('y1', (v, i) => {
            return height - yScale(v[3]) - margin.top - margin.bottom
        })
        .attr('x2', (v, i) => {
            return xScale(i) + candlestickWidth / 2
        })
        .attr('y2', (v, i) => {
            return height - yScale(v[4]) - margin.top - margin.bottom
        })
        .attr('stroke', handleStrokeColor)
        .attr('stroke-width', 1)

    // 绘制蜡烛图实线
    candlestick.append('rect')
        .attr('width', candlestickWidth)
        .attr('height', (v, i) => {
            return Math.abs(yScale(v[1]) - yScale(v[2]))
        })
        .attr('x', (v, i) => {
            return xScale(i)
        })
        .attr('y', (v, i) => {
            return height - yScale(d3.max([v[1], v[2]])) - margin.top - margin.bottom
        })
        .attr('rx', 1)
        .attr('stroke', handleStrokeColor)
        .attr('fill', (v, i) => {
            if (v[1] > v[2]) {
                return 'green'
            }

            return 'red'
        })
}

function drawFocusLayout(svg, trade_data, width, height, xScale, yScale, margin, text, formatText) {
    // 计算蜡烛图实线宽度
    const candlestickWidth = 10

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


        // 删除旧标题
        //text.selectAll('*').remove();

        text.text(formatText(trade_data[i]))
    }

    // 涨跌幅: ${v[6]}% |
    // 鼠标移出事件
    const handleMouseOut = function (e) {
        d3.select('#focusLineX').attr('display', 'none')
        d3.select('#focusLineY').attr('display', 'none')
        // console.log(trade_data.length - 1)
        console.log("123", trade_data)

        // 删除旧标题


        text.text(formatText(trade_data[trade_data.length - 1]))
    }


    // 绘制数据提示信息

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

// const data = {
//     "name": "沪深300",
//     "data": [
//         ["20220104", 4957.98, 4917.77, 4961.45, 4874.53, 15153477600, -0.46],
//         ["20220105", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01],
//         ["20220106", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01],
//         ["20220107", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01],
//         ["20220108", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01],
//         ["20220109", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01],
//         ["20220110", 4907.94, 4868.12, 4916.28, 4851.98, 17881610000, -1.01]
//     ]
// }
// var xScale = drawAxisX(trade_data)
// var yScale = drawAxisY(trade_data)


function formatText(v) {
    return `${v[0]}
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

    params.body = JSON.stringify(data);

    fetch(`/trade/${username}`, params)
        .then(response => { response.json() })
        .then(data => {
            console.log(data);
        })

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
        fetch(`/trade/${username}`, params)
            .then(response => response.json())
            .then(data => {
                console.log("DATA:", data);
                alert(data.alert);
            })
            .catch(error => console.log(error))
    });


    $("#sell-btn").click(() => {
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

        params.body = JSON.stringify(data)
        fetch(`/trade/${username}`, params)
            .then(response => response.json())
            .then(data => {
                console.log("DATA:", data);;
                alert(data.alert);
            })
            .catch(error => console.log(error))
    });

    const max_size = 10;
    var g_arr = new Array();
    var trade_data = new Array();
    const width = $("#chart").width() * 0.9;
    const height = $("#chart").height() * 0.9;
    const margin = { top: 10, right: 30, bottom: 30, left: 60 };



    const svg = d3.select('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])

    var gx = drawAxisX(svg, width, height, margin)
    var yScale = drawAxisY(svg, width, height, margin)

    // drawTitle='k线图';
    var text = svg.append('text');



    // 订阅 WebSocket 实时推送的 K 线数据

    const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@kline_1s');

    ws.onmessage = event => {
        const data = JSON.parse(event.data);
        // console.log('hightest price: ', data.k.h);
        // console.log('lowest price: ', data.k.l);
        // console.log('open price: ', data.k.o);
        // console.log('close price: ', data.k.c);
        // console.log('time:', timetrans(data.k.T));
        console.log(trade_data.length)


        text.selectAll('*').remove();
        text.attr('x', width - margin.right)
            .attr('y', margin.top / 2)
            .attr('font-size', '0.85em')
            .attr('fill', '#666')
            .attr('text-anchor', 'end')
            .attr('dominant-baseline', 'hanging')

        // 使用setTimeout函数延迟数据处理
        setTimeout(() => {
            if (trade_data.length < max_size) {
                console.log(timetrans(data.k.T))
                trade_data.push([timetrans(data.k.T), parseFloat(data.k.o), parseFloat(data.k.h), parseFloat(data.k.l), parseFloat(data.k.c)])
                // trade_data.push([timedata.k.T, parseFloat(data.k.o), parseFloat(data.k.h), parseFloat(data.k.l), parseFloat(data.k.c)])
            }

            text.text(formatText(trade_data[trade_data.length - 1]))
            // 计算蜡烛图实线宽度
            const getCandlestickWidth = dataLength => (width - margin.left - margin.right) / dataLength - 3

            drawCandlestick(svg, width, height, trade_data, gx, yScale, margin)




            drawFocusLayout(svg, trade_data, width, height, xScale, yScale, margin, text, formatText)
            // drawTitle(data.name)
        }, 1000) // 延迟500毫秒进行数据处理
    }


}
