import 'babel-polyfill'
import axios from 'axios'
import React, { useRef } from 'react'
import Highcharts from 'highcharts/highstock.src'
import darkTheme from 'highcharts/themes/brand-dark.src'
import indicator from 'highcharts/modules/price-indicator'
import { CardActionArea } from '@mui/material'
import customStyles from '../main/custom-styles'
darkTheme(Highcharts)
indicator(Highcharts)

let symbols = ['bchusdt', 'btcusdt', 'etcusdt', 'xrpusdt', 'dogeusdt', 'aaveusdt']
const animate = false
const binanceWsUrl = 'wss://fstream.binance.com/ws/'
const binanceUrl = 'https://fapi.binance.com'
const intervals = 24
const period = 5 * 1000

export const recentTrades = {}
symbols.map((s) => recentTrades[s] = undefined)

let chartWidth = (window.innerWidth - 300) / 2 - 20
if (chartWidth < 400) {
    chartWidth = 400
}

export default class Charts extends React.Component {
    constructor(props){
        super(props)
    }
    componentDidMount() {
        const charts = symbols.map(renderChart)
        updateTradeIndicator(this.props.socket, this.props.dashboardHandler, charts)
    }
    getCharts = () => {
        return symbols.map((s) => (
            <CardActionArea sx={{ width: chartWidth + 'px', margin: '2px' }} key={s}>
                <div id={'chart-' + s} onClick={() => this.selectSymbol(s)} style={this.getStyle(s)} />
            </CardActionArea>
        ))
    }
    getStyle = (s) => {
        const styles = { marginBottom: '2px' }
        if (this.props.state.selected == s) {
            return { ...styles, outline: '1px solid #FFFFBF' }
        }
        return styles
    }
    selectSymbol = (s) => {
        this.props.setState((state) => ({ ...state, selected: s }))
    }
    render = () => (
        <div style={{ width: window.innerWidth - 300, }} >
            <div className="row d-flex m-2" id='charts' >
                {this.getCharts()}
            </div>
        </div>
    )
}

function updateTradeIndicator(socket, dashboardHandler, charts) {
    socket.onmessage = async (m) => {
        const data = dashboardHandler(m)
        if (!data) return
        const positions = data.wallet.positions
        for (let i in symbols) {
            const chart = await charts[i]
            const position = positions[symbols[i]]
            const plotLine = chart.yAxis[0].options.plotLines[0]
            plotLine.value = position?.avgprice
            plotLine.color = position?.qty && position.qty > 0 ? '#AFE1AF' : '#FA8072' // celadon and salmon
            chart.yAxis[0].update()
            position && document.querySelector('#chart-' + symbols[i]).scrollIntoView()
        }
    }
}

async function renderChart(symbol) {
    const options = await getChartOptions(symbol)
    return Highcharts.stockChart('chart-' + symbol, options)
}

async function getChartOptions(symbol) {
    const res = await axios.get(binanceUrl + `/fapi/v1/aggTrades?symbol=${symbol}`)
    return {
        title: {
            text: symbol.replace('usdt', '').toUpperCase(),
            style: {
                font: '13px monospace'
            }
        },
        scrollbar: {
            enabled: false,
        },
        navigator: {
            enabled: false,
        },
        rangeSelector: {
            inputEnabled: false,
            enabled: false,
            // enable zoom by fixing it here https://github.com/highcharts/highcharts/issues/1347
        },
        yAxis: [
            {
                // candlesticks
                labels: {
                    align: 'left', // makes labels aligned to the left of the axis
                    reserveSpace: false,
                    style: {
                        font: '10px monospace',
                    },
                },
                plotLines: [{
                    value: undefined,
                    width: 1,
                    color: '#FFDD22',
                    zIndex: 10,
                }],
            },
            {
                // volume 
                visible: false,
            },
        ],
        xAxis: [{ labels: { style: { font: '10px monospace' }}}],
        chart: {
            backgroundColor: customStyles.bgcolor,
            height: chartWidth * 0.65,
            width: chartWidth,
            minWidth: 400,
            spacingRight: 50, // gives a fixed space for y axis labels to render
            events: {
                load: function () {
                    const fullUrl = binanceWsUrl + symbol + '@aggTrade'
                    new WebSocket(fullUrl).onmessage = (event) => {
                        const data = JSON.parse(event.data)
                        updateChart(data, this)
                    }
                }
            },
        },
        series: [
            {
                name: 'price',
                type: 'candlestick',
                zIndex: 1,
                color: '#F72119',
                upColor: '#39FF14',
                id: 'price',
                lastVisiblePrice: {
                    enabled: true,
                    label: {
                        enabled: true,
                        backgroundColor: '#fff01f',
                        style: {
                            color: '#000000',
                        },
                    },
                },
                data: initCandlestick(res.data),
            },
            {
                name: 'volume',
                type: 'column',
                yAxis: 1,
                zIndex: 0,
                opacity: 0.4,
                groupPadding: 0,
                pointPadding: 0,
                color: 'white',
                data: initVolume(res.data),
                animation: animate,
            }
        ],
        credits: {
            enabled: symbols.indexOf(symbol) == symbols.length - 1,
        },
    }
}

function updateChart(data, chart) {
    updateRecentTrades(data)
    updateCandlesticks(data, chart.series[0])
    updateVolume(data, chart.series[1])
}

function updateRecentTrades(data) {
    const symbol = data.s.toLowerCase()
    const price = data.p
    recentTrades[symbol] = price
}

function updateCandlesticks(data, series) {
    const currentPoint = series.data[series.data.length - 1]
    const price = parseFloat(data.p)
    const newPoint = currentPoint.x < data.T - period
    if (newPoint) {
        return series.addPoint({
            x: Math.floor(data.T / period) * period,
            open: price,
            high: price,
            low: price,
            close: price,
        }, true, series.data.length > intervals, animate)
    }
    const updates = {
        close: price,
        high: Math.max(currentPoint.high, price),
        low: Math.min(currentPoint.low, price),
    }
    currentPoint.update(updates, true, animate)
}

function updateVolume(data, series) {
    const currentPoint = series.data[series.data.length - 1]
    const volume = parseFloat(data.q) * parseFloat(data.p)
    const newPoint = currentPoint.x < data.T - period
    if (newPoint) {
        return series.addPoint({
            x: Math.floor(data.T / period) * period,
            y: volume
        }, true, series.data.length > intervals, animate)
    }
    currentPoint.update({ y: volume + currentPoint.y }, true, animate)
}

function initCandlestick(data) {
    const startInterval = Math.floor(new Date().getTime() / period) - intervals
    const output = []
    data.map((row, i) => {
        if (row.T / period < startInterval) {
            return
        }
        const price = parseFloat(row.p)
        let outputRow = output[output.length - 1]
        if (!outputRow || outputRow.x < row.T - period) {
            outputRow = newCandlestick(output, row, price)
        }
        outputRow.high = Math.max(outputRow.high, price)
        outputRow.low = Math.min(outputRow.low, price)
        outputRow.close = price
    })
    return output
}

function initVolume(data) {
    const startInterval = Math.floor(new Date().getTime() / period) - intervals
    const output = []
    data.map((row, i) => {
        if (row.T / period < startInterval) {
            return
        }
        const quantity = parseFloat(row.q) * parseFloat(row.p)
        let outputRow = output[output.length - 1]
        if (!outputRow || outputRow.x < row.T - period) {
            outputRow = newColumn(output, row, quantity)
        }
        outputRow.y += quantity
    })
    return output
}

function newCandlestick(output, row, price) {
    output.push({
        x: Math.floor(row.T / period) * period,
        open: price,
        high: price,
        low: price
    })
    return output[output.length - 1]
}

function newColumn(output, row, y) {
    output.push({
        x: Math.floor(row.T / period) * period,
        y,
    })
    return output[output.length - 1]
}