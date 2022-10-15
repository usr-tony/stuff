import { CircularProgress } from "@mui/material"
import React, { useEffect, useState, useMemo } from "react"
import { jobsUrl } from "./jobs"
import { bubbles } from './charts'
import Highcharts from 'highcharts'
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
HighchartsMore(Highcharts);
darkTheme(Highcharts);


let keywordsUrl = jobsUrl + '/keywords'

export default function({ useGlobalState }) {
    const [globals, _] = useGlobalState
    const [state, setState] = useState({currentChart: null})
    let key = JSON.stringify(globals.filters)
    useMemo(() => {
        let data = state?.[key]?.data
        if (!data && key != '{}') {
            getData(key, setState)
        }
    }, [globals.filters])
    useEffect(() => {
        const data = state?.[key]?.data
        renderChart(data)
    }, [key, state?.[key]])
    return (
        <div id='keywords' className='jobs-chart'>
            {state?.[key]?.loading && <CircularProgress />}
            {key == '{}' && <div>No filters selected</div> }
        </div>
    )
}

var chart = null
async function renderChart(data) {
    try {
        chart.destroy()
    } catch {}
    if (!data) {
        return
    }
    chart = Highcharts.chart(
        'keywords', 
        bubbles(data, () => {}, 'Keywords calculated using tf-idf', false)
    )
}

async function getData(key, setState) {
    setState((state) => 
        setKeyValue(key, state, { loading: true })
    )
    const response = await fetch(keywordsUrl, {
        method: "POST",
        mode: "cors",
        body: key,
    })
    const data = await response.json()
    setState((state) => 
        setKeyValue(key, state, { loading: false, data })
    )
}

function setKeyValue(key, state, value) {
    if (state?.[key]?.data?.length) {
        return state
    }
    return { ...state, [key]: value }
}