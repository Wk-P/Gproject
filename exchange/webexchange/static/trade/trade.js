function timetrans(date) {
    var date = new Date(date);//如果date为13位不需要乘1000
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    var D = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()) + ' ';
    var h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
    var m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
    var s = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
    return Y + M + D + h + m + s;
}

window.onload = () => {


    // 定义画布宽度、高度和边距
    const width = $("#chart").width() * 0.9;
    const height = $("#chart").height() * 0.9;
    const margin = { top: 10, right: 30, bottom: 30, left: 60 };

  
    // 创建SVG元素
    const svg = d3.select('#chart')
        .append('svg')
        .attr('width', width,)
        .attr('height', height,);




    // 获取当前交易对的价格
    // const symbol = 'BTC_USDT';
    // fetch(`https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`, { mode: 'cors' })
    //     .then(response => response.json())
    //     .then(data => console.log(`当前 ${symbol} 价格为 ${data.price}`))
    //     .catch(error => console.error(error));


    
    // 订阅 WebSocket 实时推送的 K 线数据
    const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@kline_1s');




    ws.onmessage = event => {
        const data = JSON.parse(event.data);
        console.log('hightest price：', data.k.h);
        console.log('lowest price：', data.k.l);
        console.log('open price：', data.k.o);
        console.log('close price：', data.k.c);
        console.log('time:', timetrans(data.k.T));
        const trade_data = [
            { time: timetrans(data.k.T), open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c },
            { time: timetrans(data.k.T), open: data.k.o, high: data.k.h, low: data.k.l, close: data.k.c },
            // { time: '2021-01-03', open: 10500, high: 11000, low: 10000, close: 10200 },
        

        ];

        // 定义K线图的比例尺和坐标轴
        const xScale = d3.scaleBand().range([margin.left, width - margin.right]);
        const yScale = d3.scaleLinear().range([height - margin.bottom, margin.top]);
        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);

        // 更新K线图
        const updateChart = (trade_data) => {
            // 计算比例尺的域
            const minTime = d3.min(trade_data, d => d.time);
            const maxTime = d3.max(trade_data, d => d.time);
            const minValue = d3.min(trade_data, d => d.low);
            const maxValue = d3.max(trade_data, d => d.high);


            // 更新比例尺的域
            xScale.domain(trade_data.map(d => new Date(d.time)));
            yScale.domain([minValue, maxValue]);

            // 添加坐标轴
            svg.select('.x-axis')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(xAxis);



            svg.select('.y-axis')
                .attr('transform', `translate(${margin.left}, 0)`)
                .call(yAxis);

            // 更新K线图的数据
            const candles = svg.selectAll('.candle').data(trade_data);

            // 移除已经不存在的数据
            candles.exit().remove();

            // 添加新的K线图数据
            const newCandles = candles.enter()
                .append('g')
                .attr('class', 'candle')
                .attr('transform', d => `translate(${xScale(new Date(d.time)) - xScale.bandwidth() / 20}, 0)`);


            var color = 'green';
            newCandles.append('line')
                .attr('class', 'high-low')
                .attr('x1', xScale.bandwidth() / 5)
                .attr('x2', xScale.bandwidth() / 5)
                .attr('y1', d => yScale(d.high))
                .attr('y2', d => yScale(d.low))
                .attr('stroke', d => d.open < d.close ? 'green' : 'red');

            var color_two = 'red';

            newCandles.append('rect')
                .attr('class', 'open-close')
                .attr('x', 0)
                .attr('y', d => yScale(Math.max(d.open, d.close)))
                .attr('width', xScale.bandwidth() / 5)   //柱宽
                .attr('fill', d => d.open < d.close ? 'green' : 'red')
                .attr('height', d => {
                    if (d.open === d.close) {
                        return 1;
                    } else {
                        return yScale(Math.min(d.open, d.close)) - yScale(Math.max(d.open, d.close));
                    }
                });

                // 更新K线图的位置和大小
                candles.merge(newCandles)
                .transition()
                .duration(1000)
                .attr('transform', d => `translate(${xScale(new Date(d.time)) - xScale.bandwidth() / 20}, 0)`);
              
              candles.merge(newCandles)
                .select('.high-low')
                .transition()
                .duration(1000)
                .attr('y1', d => yScale(d.high))
                .attr('y2', d => yScale(d.low))
                .attr('stroke', d => d.open < d.close ? color : color_two);
              
              candles.merge(newCandles)
                .select('.open-close')
                .transition()
                .duration(1000)
                .attr('y', d => yScale(Math.max(d.open, d.close)))
                .attr('height', d => d.open === d.close ? 1 : Math.abs(yScale(d.open) - yScale(d.close)))
                .attr('fill', d => d.open < d.close ? color : color_two);
                

            }
        updateChart(trade_data)
        // console.log(updateChart);

        // 选中DOM元素并添加事件监听
        $('#time-buttons button').on('click', function () {
            // 处理事件
        });





        // 连接服务器
        // const socket = io.connect('http://localhost');

        // 监听事件
        // socket.on('update', function (data) {
        // 更新数据
        // });
    }
}     