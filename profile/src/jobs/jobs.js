import React, { useState } from "react";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
import "babel-polyfill";
import { CircularProgress, Alert } from "@mui/material";
import { columns, bubbles } from './charts'
import SideSection from './side-section'
HighchartsMore(Highcharts);
darkTheme(Highcharts);


export let jobsUrl = "https://g0ud4ex9ui.execute-api.ap-southeast-2.amazonaws.com/jobs";
var jobsChart = null

export default function ({ useGlobalState }) {
    const [state, setState] = useGlobalState
    const [loading, setLoading] = useState(true)
    if (loading) {
        if (jobsChart) {
            jobsChart.destroy()
        }
        renderChart(state, setState, setLoading).then(chart => jobsChart = chart);
    }
    return (
        <div className="d-flex flex-direction-row">
            <div>
                <div id="jobs" className="jobs-chart">
                    {loading && <CircularProgress />}
                </div>
                {state.by && 
                    <Alert 
                        variant="standard" 
                        severity='info' 
                        sx={{fontSize: '1rem'}}
                    >
                        click on the graph to filter
                    </Alert>
                }
            </div>
            <SideSection state={state} setLoading={setLoading} setState={setState} />
        </div>
    );
}

async function renderChart(state, setState, setLoading) {
    const data = await getData(state, setLoading);
    const title = getJobsChartTitle(state)
    const clickEvent = (value) => {
        if (state.period && Object.keys(state.filters).length) {
            return
        }
        setState(state => ({
            period: "day",
            filters: { [state.by]: value },
            type: "columns",
        }))
        setLoading(true)
    }
    const optionsGenerator = state.type == 'bubbles' ? bubbles : columns
    return Highcharts.chart(
        'jobs', 
        optionsGenerator(data, clickEvent, title)
    )
}

function getJobsChartTitle(state) {
    if (state.by) {
        return `jobs by ${state.by}`
    }
    const periodText = state.period == "day" ? "daily" : "weekly";
    return `${periodText} job postings over time`;
}

async function getData(state, setLoading, url=jobsUrl) {
    const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(state),
    });
    setLoading(false)
    let data = await response.json();
    if (state.type == 'columns') {
        return columnarJobsData(data, state)
    }
    return shortenNamesForBubbles(data)
}

function shortenNamesForBubbles(data) {
    return data.map((row) => {
        let words = row[0].replace(',', '').split(' ')
        row.splice(1, 0, words[0]) // find another way to modify tooltip and datalabels separately
        return row
    })
}

function columnarJobsData(data, state) {
    let categories = data.map(row => {
        const ts = row[0] || ''
        return state.by ? ts : ts2date(ts)
    })
    let heights = data.map(row => row[1])
    return [categories, heights]
}

function ts2date(ts) {
    return new Date(ts * 1000)
        .toLocaleDateString('en-US', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
        })
}