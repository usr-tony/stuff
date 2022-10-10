import { CircularProgress } from "@mui/material"
import React, { useEffect, useState } from "react"
import { jobsUrl } from "./jobs"
import { bubbles } from './charts'
import Highcharts from 'highcharts'
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
HighchartsMore(Highcharts);
darkTheme(Highcharts);


let keywordsUrl = jobsUrl + '/keywords'

var chart = null
export default function({ useGlobalState }) {
    const [globalState, _] = useGlobalState
    const [loading, setLoading] = useState(true)
    useEffect(() => {
        setLoading(true)
    }, [globalState.filters])
    if (loading) {
        if (chart) {
            chart.destroy()
        }
        renderChart(globalState, setLoading).then(e => chart = e)
    }
    const noFilters = !Object.keys(globalState.filters).length
    return (
        <div id='keywords' className='jobs-chart'>
            {loading && !noFilters && <CircularProgress />}
            {noFilters && <div>no filters selected</div>}
        </div>
    )
}

async function renderChart(state, setLoading) {
    if (!Object.keys(state.filters).length) {
        return
    }
    const data = await getData(state, setLoading)
    return Highcharts.chart(
        'keywords', 
        bubbles(data, () => {}, 'Top keywords from filtered jobs', false)
    )
}

async function getData(state, setLoading) {
    const response = await fetch(keywordsUrl, {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(state.filters),
    })
    const data = await response.json()
    setLoading(false)
    return data
}