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
        try{
            chart.destroy()
        } catch {}
        renderChart(globalState, setLoading).then(e => chart = e)
    }
    const noFilters = !Object.keys(globalState.filters).length
    return (
        <div id={getId(globalState)} className='jobs-chart'>
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
    try {
        return Highcharts.chart(
            getId(state), 
            bubbles(data, () => {}, 'Top keywords from filtered jobs, calculated using tf-idf', false)
        )
    } catch {
        return null
    }
    
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

function getId (state) {
    return 'keywords' + JSON.stringify(state.filters)
}