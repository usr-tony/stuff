import React, { useState } from "react";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
import "babel-polyfill";
import { Button, CircularProgress, Alert, generateUtilityClass } from "@mui/material";
import { columns, bubbles } from './charts'
HighchartsMore(Highcharts);
darkTheme(Highcharts);

var chart = null
export default () => {
    const [state, setState] = useState({
        by: "sector",
        filters: {},
        loading: true,
        type: "bubbles",
    });
    const props = { setState, state };
    if (state.loading) {
        try {
            chart.destroy()
        } catch (e) {
            console.log(e)
        }
        renderCharts().then(e => chart = e);
    }

    async function renderCharts() {
        let options = null;
        if (state.by) {
            if (state.type == "columns") options = await columns(state, setState);
            else options = await bubbles(state, setState);
        } else if (state.period) {
            options = await columns(state, setState);
        }
        return Highcharts.chart("jobs", options);
    }
    return (
        <div className="d-flex flex-direction-row">
            <div>
                <div id="jobs" className="jobs-chart">
                {state.loading && <CircularProgress />}
                </div>
                {
                    state.by && 
                    <Alert 
                        variant="standard" 
                        severity='info' 
                        sx={{fontSize: '1rem'}}
                    >
                        click on the graph to filter
                    </Alert>
                }
            </div>
            <SideSection props={props} />
        </div>
    );
};

function SideSection({ props }) {
    return (
        <div>
            grouped data:
            <div>
                <ByButton {...{ ...props, by: "company" }} />
                <ByButton {...{ ...props, by: "sector" }} />
                <ByButton {...{ ...props, by: "state" }} />
            </div>
            periodic data:
            <div>
                <PeriodData {...{ ...props, period: "day" }} />
                <PeriodData {...{ ...props, period: "week" }} />
            </div>
            chart type:
            <div>
                <ChartType {...{ ...props, type: "columns" }} />
                <ChartType
                    {...{ ...props, type: "bubbles" }}
                />
            </div>
            <DisplayFilters {...props} />
        </div>
    );
}
const buttonStyle = {
    width: 50
}
const selectedButtonStyle = {
    buttonStyle,
    backgroundColor: 'green',
}
function ByButton({ by, setState, state }) {
    function onClick() {
        setState((state) => ({ type: state.type, by, loading: true }));
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

function PeriodData({ period, setState, state }) {
    function onClick() {
        setState((state) => {
            const newState = {
                filters: state.filters,
                period, 
                type: 'columns', 
                loading: true,
            }
            delete newState.by
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

function ChartType({ type, state, setState }) {
    function onClick() {
        setState((state) => ({ ...state, loading: true, type }));
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

function DisplayFilters(props) {
    const filters = props.state.filters
    if (!filters || !Object.keys(filters).length) {
        return <div></div>
    }
    return (
        <>
            <div>filters:</div>
            {GenerateFilters(filters)}
        </>
    )
}

function GenerateFilters(filters) {
    const elements = []
    for (let key in filters) {
        elements.push(<div key={key}>{key}: {filters[key]}</div>)
    }
    return elements
} 
