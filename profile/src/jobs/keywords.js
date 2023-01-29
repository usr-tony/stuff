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

export default function ({ useGlobalState }) {
    const [globals, _] = useGlobalState
    const [state, setState] = useState({})
    let key = JSON.stringify(globals.filters)
    useEffect(() => {
        if (key == '{}') return
        getData(key, state, setState)
    }, [key])
    useEffect(() => renderChart(state[key]?.data), [state, key])
    return (
        <div key={key}>
            <div id='keywords' className='jobs-chart' >
                {state?.[key]?.loading && <CircularProgress />}
                {key == '{}' && <div>No filters selected</div>}
            </div>
        </div>
    )
}

async function renderChart(data) {
    if (!data) {
        return
    }
    Highcharts.chart(
        'keywords',
        bubbles(data, () => { }, 'Keywords calculated using tf-idf', false)
    )
}

async function getData(key, state, setState) {
    if (state?.[key]?.data) {
        return
    }
    setState((state) =>
        setKeyValue(key, state, { loading: true })
    )
    let response = null
    while (response?.status != 200) {
        try {
            response = await fetch(keywordsUrl, {
                method: "POST",
                mode: "cors",
                body: key,
            })
        } catch { }

    }
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