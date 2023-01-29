import React, { useState } from "react"
import { Drawer, Button, TableContainer, Table, TableHead, TableBody, TableRow, TableCell, Switch, Alert } from '@mui/material'
import { recentTrades } from "./charts"

export default ({ socket, state }) => {
    function toggleAuto() {
        if (!state.auto)
            socket.send('auto')
        else 
            socket.send('stop auto')
    }
    function trade(side) {
        if (!state.selected) {
            // add an indicator
            return 
        }
        if (!recentTrades[state.selected]) {
            return
        }
        socket.send(JSON.stringify({
            symbol: state.selected,
            side,
            lastprice: recentTrades[state.selected]
        }))
    }
    return (
        <>
            <Drawer anchor="right" variant="permanent"
                sx={{
                    '& .MuiDrawer-paper': { width: 300, boxSizing: 'border-box' },
                }}
            >
                <Wallet data={state.status.wallet} />
                <Stats data={state.status.stats} />
                <div style={{ position: 'absolute', bottom: 25, width: '100%' }} >
                    <Switch disabled={!state.live} checked={state.live} /> live
                    <TradeButton text="Auto" color="primary" onClick={toggleAuto} />
                    <div className="d-flex">
                        <TradeButton text="Buy" color="success" disabled={state.auto} onClick={() => trade('buy')} />
                        <TradeButton text="Sell" color="error" disabled={state.auto} onClick={() => trade('sell')} />
                    </div>
                </div>
            </Drawer>
        </>
    )
}

function Wallet(props) {
    return (
        <TableContainer component={null} sx={{ height: 400 }}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>
                            Symbol
                        </TableCell>
                        <TableCell>
                            Quantity
                        </TableCell>
                        <TableCell>
                            Average Price
                        </TableCell>
                        <TableCell>
                            Profit
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.data.map((row, i) => (
                        <TableRow key={i}>
                            <TableCell>{row.symbol}</TableCell>
                            <TableCell>{row.qty}</TableCell>
                            <TableCell>{row.avgprice}</TableCell>
                            <TableCell>{row.profit}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

function Stats(props) {
    return (
        <TableContainer component={null}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>
                            Gross Profit
                        </TableCell>
                        <TableCell>
                            Fees
                        </TableCell>
                        <TableCell>
                            Net Profit
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.data.map((row, i) => (
                        <TableRow key={i}>
                            <TableCell>{row.gp}</TableCell>
                            <TableCell>{row.fees}</TableCell>
                            <TableCell>{row.np}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

function TradeButton(props) {
    return (
        <div className="m-2 col">
            <Button variant="contained" fullWidth={true} {...props} >
                {props.text}
            </Button>
        </div>
    )
}