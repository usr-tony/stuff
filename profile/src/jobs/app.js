import React, { useState } from "react";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
import "babel-polyfill";
import Jobs from './jobs'
import Keywords from './keywords'
HighchartsMore(Highcharts);
darkTheme(Highcharts);


export default () => {
    let useGlobalState = useState({
        by: "sector",
        filters: { sector: 'Information & Communication Technology' },
        type: "bubbles",
    })
    return <>
        <Jobs useGlobalState={useGlobalState} />
        <Keywords useGlobalState={useGlobalState} />
    </>
}

