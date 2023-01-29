import React, { useState, useEffect } from "react";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
import "babel-polyfill";
import { CircularProgress, Alert, Paper } from "@mui/material";
import { columns, bubbles } from './charts'
import SideSection from './side-section'
HighchartsMore(Highcharts);
darkTheme(Highcharts);


export const jobsUrl = "https://g0ud4ex9ui.execute-api.ap-southeast-2.amazonaws.com/jobs";

export default function ({ useGlobalState }) {
    const [state, setState] = useGlobalState
    const [loading, setLoading] = useState(false)
    useEffect(() => {
        renderChart(state, setState, setLoading)
    }, [state])
    return (
        <div className="d-flex flex-direction-row" key={JSON.stringify(state)} >
            <div>
                <div id="jobs" className="jobs-chart">
                    {loading && <CircularProgress />}
                </div>
                {state.by &&
                    <Alert
                        variant="standard"
                        severity='info'
                        sx={{ fontSize: '1rem' }}
                    >
                        click on the graph to drill down and show keywords
                    </Alert>
                }
            </div>
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
            period: "month",
            filters: { [state.by]: value },
            type: "columns",
        }))
        setLoading(true)
    }
    const optionsGenerator = state.type == 'bubbles' ? bubbles : columns
    try {
        return Highcharts.chart(
            'jobs',
            optionsGenerator(data, clickEvent, title)
        )
    } catch { }
}

function getJobsChartTitle(state) {
    if (state.by) {
        return `Jobs posted by ${state.by}`
    }
    const periodText = {
        day: 'Daily',
        week: 'Weekly',
        month: 'Monthly',
    }[state.period]
    return `${periodText} job postings over time`;
}

async function getData(state, setLoading, url = jobsUrl) {
    setLoading(true)
    let response = null
    let retries = 0
    while (response?.status != 200) {
        try {
            response = await fetch(url, {
                method: "POST",
                mode: "cors",
                body: JSON.stringify(state),
            });
        } catch { 
            if (retries++ > 3) break
        }
    }
    let data = await response.json();
    setLoading(false)
    if (state.type == 'columns') {
        return columnarData(data, state)
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

function columnarData(data, state) {
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