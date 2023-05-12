window.onload = () => {
  const width = 1000
  const height = 500
  const margin = { top: 50, right: 30, bottom: 30, left: 80 }

  const svg = d3.select('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', [0, 0, width, height])

  // 计算蜡烛图实线宽度
  const getCandlestickWidth = dataLength => (width - margin.left - margin.right) / dataLength - 3

  // 绘制标题
  function drawTitle(value) {
    const title = svg.append('text')
      .text(value)
      .attr('x', margin.left)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'start')
      .attr('dominant-baseline', 'hanging')
  }

  // 绘制横坐标
  function drawAxisX(data) {
    const dates = d3.map(data, v => v[0])

    const scale = d3.scaleLinear()
      .domain([0, data.length])
      .range([0, width - margin.left - margin.right])

    const axis = d3.axisBottom(scale)
      .ticks(10)
      .tickFormat(v => {
        return dates[v]
      })

    svg.append('g')
      .attr('transform', 'translate(' + margin.left + ',' + (height - margin.bottom) + ')')
      .call(axis)

    return scale
  }

  // 绘制竖标轴
  function drawAxisY(data) {
    // 找到最高价和最低价，用来作为蜡烛图的参照坐标
    const highPrices = d3.map(data, v => v[3])
    const lowPrices = d3.map(data, v => v[4])
    const pricePending = Math.round(d3.max(highPrices) / 100)

    // 绘制竖坐标
    const scale = d3.scaleLinear()
      .domain([d3.min(lowPrices) - pricePending, d3.max(highPrices) + pricePending])
      .range([0, height - margin.top - margin.bottom])

    const axis = d3.axisLeft(scale).ticks(10)

    svg.append('g')
      .attr('transform', 'translate(' + (margin.left - 5) + ', ' + margin.top + ')')
      .call(axis)
      .call(g => g.select('.domain').remove())
      .call(g => {
        g.selectAll('.tick line')
          .clone()
          .attr('stroke-opacity', 0.1)
          .attr('stroke-dasharray', 5)
          .attr('x2', width - margin.left - margin.right)
      })

    return scale
  }

  // 获取数据并开始绘制
  d3.json('/data.json').then(data => {
    const xScale = drawAxisX(data.data)
    const yScale = drawAxisY(data.data)

    drawTitle(data.name)
  })
}


