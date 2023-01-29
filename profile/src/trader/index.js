import React, { useState } from 'react'
import 'babel-polyfill'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Charts from './charts'
import TradingDashboard from './trading-dashboard'
import Breadcrumbs from './breadcrumbs'
import customStyles from '../main/custom-styles'

const socket = new WebSocket('wss://3.26.228.56:8050') // connects to the backend aws ec2 instance for all trades

const theme = createTheme({
    palette: {
        mode: 'dark',
    },
    typography: {
        fontFamily: customStyles.fontFamily,
        button: {
            textTransform: 'none',
            fontSize: 12,
        },
        fontSize: 10,
    }
});

export default () => {
    const [state, setState] = useState({
        selected: undefined,
        live: false,
        auto: false,
        status: { wallet: [], stats: [] },
    })
    
    return (
        <ThemeProvider theme={theme}>
            <Breadcrumbs />
            <Charts state={state} setState={setState} socket={socket} dashboardHandler={(m) => dashboardHandler(m, setState)} />
            <TradingDashboard socket={socket} state={state} />
        </ThemeProvider>
    )
}

function dashboardHandler(m, setState) {
    if (m.data == 'live') {
        return setState((state) => ({ ...state, live: true }))
    } 
    if (m.data == 'auto trader started') {
        return setState((state) => ({ ...state, auto: true }))
    }
    if (m.data == 'auto trader stopped') {
        return setState((state) => ({ ...state, auto: false}))
    }
    try {
        var data = JSON.parse(m.data)
    } catch (e) {
        return
    }
    const wallet = [{ symbol: 'cash', qty: data.wallet.cash }]
    const positions = data.wallet.positions
    for (let symbol in positions) {
        // positions[symbol] contains qty and avgprice
        wallet.push({ symbol, ...positions[symbol] })
    }
    setState((state) => ({
        ...state,
        status: {
            wallet,
            stats: [ data.stats ],
        }
    }))
    return data
}



