import React from "react";
import { Button, Typography } from "@mui/material";


const buttonStyle = {
    width: 50
}
const selectedButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#90EE90',
    '&:hover': {
        backgroundColor: '#70CC70'
    }
}

const textStyle = {
    marginLeft: '0.5rem',
    fontSize: '0.8rem'
}

export default (props) => {
    return (
        <div>
            <div>
                <ButtonGroup text='Group jobs by:'>
                    <ByButton {...props} by='company' />
                    <ByButton {...props} by='sector' />
                    <Typography sx={textStyle} >
                        Then click on the graph to drill down
                    </Typography>
                </ButtonGroup>
                <ButtonGroup text='Show job trends by:'>
                    <PeriodButton {...props} period='day' />
                    <PeriodButton {...props} period='week' />
                    <PeriodButton {...props} period='month' />
                </ButtonGroup>
                <ButtonGroup text='Select chart type'>
                    <ChartTypeButton {...props} type='columns' />
                    <ChartTypeButton {...props} type='bubbles' />
                </ButtonGroup>
            </div>
            <DisplayFilters {...props} />
        </div>
    );
}

function ButtonGroup({ text, children }) {
    return (
        <div style={{ marginBottom: '1rem' }}>
            <Typography sx={textStyle} marginBottom='0'>
                {text}
            </Typography>
            {children}
        </div>
    )
}

export function ByButton({ by, state, setState }) {
    function onClick() {
        setState({ by, type: state.type, filters: {} }); // resets all filters
    }
    return (
        <Button
            variant="contained"
            className="m-2"
            sx={by == state.by ? selectedButtonStyle : buttonStyle}
            onClick={onClick}
        >
            {by}
        </Button>
    );
}

export function PeriodButton({ period, setState, state }) {
    function onClick() {
        setState((state) => {
            const newState = {
                filters: state.filters,
                period, 
                type: 'columns', 
            }
            return newState
        });
    }
    return (
        <Button
            variant="contained"
            className="m-2"
            sx={period == state.period ? selectedButtonStyle : buttonStyle}
            onClick={onClick}
        >
            {period}
        </Button>
    );
}

export function ChartTypeButton({ type, state, setState }) {
    function onClick() {
        setState((state) => ({ ...state, type }));
    }
    return (
        <Button
            variant="contained"
            className="m-2"
            sx={type == state.type ? selectedButtonStyle : buttonStyle}
            onClick={onClick}
            disabled={type == 'bubbles' && Boolean(state.period)}
        >
            {type}
        </Button>
    );
}

export function DisplayFilters(props) {
    const filters = props.state.filters
    if (!filters || !Object.keys(filters).length) {
        return <></>
    }
    return (
        <>
            <Typography sx={textStyle}>Filters applied:</Typography>
            {GenerateFilters(filters)}
        </>
    )
}

function GenerateFilters(filters) {
    const elements = []
    for (let key in filters) {
        elements.push(<Typography sx={textStyle} key={key}>{key}: {filters[key]}</Typography>)
    }
    return elements
} 
