

const margin = { top: 10, right: 30, bottom: 30, left: 60 };

// 绘制标题
function drawTitle( svg, margin) {
    svg.append('text')
        .text('k')
        .attr('x', margin.left)
        .attr('y', margin.top / 2)
        .attr('text-anchor', 'start')
        .attr('dominant-baseline', 'hanging')
}




function timetrans(date) {
    var date = new Date(date); //如果date为13位不需要乘1000
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

    //var yExtent=[0,100]; //设置y轴取值范围
    var scaleY=d3.scaleLinear()
    .range([0,height-margin.top-margin.bottom]) //生成比例尺
    const axisY = d3.axisLeft(scaleY).ticks(100); //生成轴线
    var gY = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(axisY)
    return gY
}

function drawCandlestick(svg, width, height, trade_data, gx, gY, margin) {
    console.log(trade_data)
    const highPrices = d3.map(trade_data, v => v[2])
    const lowPrices = d3.map(trade_data, v => v[3])
    const pricePending = Math.round(d3.max(highPrices) / 100)

    var dates = d3.map(trade_data, v => v[0])

    // const parseTime = d3.timeParse('%s');
    // dates = dates.map(d => parseTime(d));
    console.log(dates)

    let datesObjects = []
    for (let i = 0; i < 10; i++) {
        if (i < length) {
            datesObjects[i] = dates[i]
        }
        else {
            datesObjects[i] = parseInt(dates[0]) + i;
        }
    }

    const xScale = d3.scaleLinear()
        .domain([parseInt(datesObjects[0]), parseInt(datesObjects[datesObjects.length - 1])])
        .range([0, width - margin.left - margin.right])

    const xaxis = d3.axisBottom(xScale)
        .tickValues(datesObjects)
        .tickFormat(d3.format("d"))
    gx.call(xaxis);


    // 定义新的x轴比例尺

    // 更新x轴比例尺属性

    const yScale = d3.scaleLinear()
    .domain([d3.max(highPrices) + pricePending, d3.min(lowPrices) - pricePending])
    .range([height - margin.bottom,margin.top ])

    const yaxis = d3.axisLeft(yScale)
        .ticks(20)
        .tickFormat(d3.format(".2f"))
    gY.call(yaxis);


   // gY.domain([d3.max(highPrices) + pricePending, d3.min(lowPrices) - pricePending])
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

    const candlestick = svg.selectAll('g')
        .data(trade_data)
        .enter()
        .append('g')

        candlestick.append('line')
        .attr('x1', (v, i) => {
            return xScale(i) + (1 - candlestickWidth) / 2
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
        console.log('text')
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
                console.log("DATA:", data);
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
        
    const yExtent=[0,100]; //设置y轴取值范围

    const svg = d3.select('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height])

    var gx = drawAxisX(svg, width, height, margin)
    var gY = drawAxisY(svg, width, height, margin)

    // drawTitle='k线图';
    var text = svg.append('text');

    console.log(trade_data.length)
    drawTitle(svg,margin)
    

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
                    console.log(data.price_data);
                    if (trade_data.length > max_size) {
                        trade_data.shift()
                    }
                    trade_data.push([timetrans(data.price_data.k.T), 
                        parseFloat(data.price_data.k.o), 
                        parseFloat(data.price_data.k.h), 
                        parseFloat(data.price_data.k.l), 
                        parseFloat(data.price_data.k.c)])

                    text.text(formatText(trade_data[trade_data.length - 1]))
                    // 计算蜡烛图实线宽度
                    const getCandlestickWidth = dataLength => (width - margin.left - margin.right) / dataLength - 3

                    drawCandlestick(svg, width, height, trade_data, gx,gY, margin)

                 //   drawFocusLayout(svg, trade_data, width, height, xScale, yScale, margin, text, formatText)
                }) // 延迟500毫秒进行数据处理
        }, 1000)
    }
    catch (error) {
        console.error(error)
    }
}
